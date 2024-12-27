from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Self, Any, Literal, Optional
from abc import ABC, abstractmethod
import json
import asyncio
import functools
import logging

from paho.mqtt.client import Client as PahoClient
from paho.mqtt.enums import CallbackAPIVersion

from ki2_python_utils import is_json

from .DualContextCallback import DualContextCallback
from .EventData import OnConnectEvent, OnDisconnectEvent, OnMessageEvent
from .TopicCallback import TopicsMessageCallback

if TYPE_CHECKING:
    from paho.mqtt.client import ConnectFlags, DisconnectFlags, MQTTMessage, SocketLike
    from paho.mqtt.reasoncodes import ReasonCode
    from paho.mqtt.properties import Properties

    from ki2_python_utils import Json

    from .DualContextCallback import DualContextCallbackType

logger = logging.getLogger(__name__)


class AbstractSimpleMqtt(ABC):
    """
    Abstract base class for managing MQTT clients, supporting both synchronous
    and asynchronous operations.

    This class provides fundamental methods for connecting, subscribing, and
    publishing messages using the Paho MQTT client.
    """

    _client: PahoClient
    _default_qos: int

    _started: bool

    _pending_subscriptions: list[tuple[str, int]]

    _on_connect: DualContextCallback[OnConnectEvent]
    _on_disconnect: DualContextCallback[OnDisconnectEvent]
    _on_message: DualContextCallback[OnMessageEvent]
    _on_topic_message: TopicsMessageCallback

    def __init__(self):
        """
        Initializes the AbstractSimpleMqtt instance.

        Sets up the MQTT client, event callbacks, and default configurations.
        """
        self._default_qos = 0
        self._pending_subscriptions = []
        self._started = False

        self._on_connect = DualContextCallback()
        self._on_disconnect = DualContextCallback()
        self._on_message = DualContextCallback()
        self._on_topic_message = TopicsMessageCallback()

        self._client = PahoClient(CallbackAPIVersion.VERSION2)

        self._client.on_connect = self.__on_paho_connect_event
        self._client.on_disconnect = self.__on_paho_disconnect_event
        self._client.on_message = self.__on_paho_message_event

    @property
    def default_qos(self):
        """
        Retrieves the default QoS level for subscriptions and publications.

        Returns:
            int: The default QoS level.
        """
        return self._default_qos

    @property
    def is_connected(self):
        """
        Checks if the client is currently connected to the broker.

        Returns:
            bool: True if connected, False otherwise.
        """
        return self._client.is_connected()

    @property
    def started(self):
        """
        Checks if the MQTT client connection has been started.

        Returns:
            bool: True if started, False otherwise.
        """
        return self._started

    def set_default_qos(self, qos: int) -> Self:
        """
        Sets the default QoS level for future subscriptions and publications.

        Args:
            qos (int): The desired QoS level.

        Returns:
            Self: The current instance for method chaining.
        """
        logger.info(f"Setting default QoS to {qos}")
        self._default_qos = qos
        return self

    def on_connect(self, callback: DualContextCallbackType[OnConnectEvent]) -> Self:
        """
        Registers a callback for connection events.

        Args:
            callback (DualContextCallbackType[OnConnectEvent]): The callback to
                register.

        Returns:
            Self: The current instance for method chaining.
        """
        self._on_connect.add(callback)
        return self

    def on_disconnect(
        self, callback: DualContextCallbackType[OnDisconnectEvent]
    ) -> Self:
        """
        Registers a callback for disconnection events.

        Args:
            callback (DualContextCallbackType[OnDisconnectEvent]): The callback to
                register.

        Returns:
            Self: The current instance for method chaining.
        """
        self._on_disconnect.add(callback)
        return self

    def on_message(self, callback: DualContextCallbackType[OnMessageEvent]) -> Self:
        """
        Registers a callback for general message events.

        Args:
            callback (DualContextCallbackType[OnMessageEvent]): The callback to
                register.

        Returns:
            Self: The current instance for method chaining.
        """
        self._on_message.add(callback)
        return self

    def on_topic_message(
        self,
        topic: str,
        callback: DualContextCallbackType[OnMessageEvent],
        qos: int = 0,
    ) -> Self:
        """
        Registers a callback for a specific topic.

        Args:
            topic (str): The topic to associate with the callback.
            callback (DualContextCallbackType[OnMessageEvent]): The callback to
                register.
            qos (int, optional): The QoS level for the subscription. Defaults to 0.

        Returns:
            Self: The current instance for method chaining.
        """
        self._on_topic_message.add(topic, callback)
        self.subscribe_sync(topic, qos)
        return self

    def subscribe_sync(self, topic: str, qos: int = 0) -> Self:
        """
        Subscribes to a topic synchronously.

        Args:
            topic (str): The topic to subscribe to.
            qos (int, optional): The QoS level for the subscription. Defaults to 0.

        Returns:
            Self: The current instance for method chaining.
        """
        logger.debug(f"[sync] Subscribing to '{topic}' with QoS {qos}")
        if self.is_connected:
            result, _ = self._client.subscribe(topic, qos)
            if result != 0:
                logger.warning(
                    f"[sync] Failed to subscribe to topic '{topic}',"
                    f" result code: {result}"
                )
        else:
            logger.info(
                f"[sync] Client not connected. Deferring subscription to '{topic}'"
            )
            self._pending_subscriptions.append((topic, qos))
        return self

    def connect_sync(
        self,
        hostname: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
        bind_port: int = 0,
        clean_start: bool | Literal[3] = 3,
        properties: Properties | None = None,
        *,
        username: str | None = None,
        password: str | None = None,
    ):
        """
        Connects to an MQTT broker synchronously.

        Args:
            hostname (str): The broker hostname.
            port (int, optional): The broker port. Defaults to 1883.
            keepalive (int, optional): Keepalive interval in seconds. Defaults to 60.
            bind_address (str, optional): Local bind address. Defaults to "".
            bind_port (int, optional): Local bind port. Defaults to 0.
            clean_start (bool | Literal[3], optional): Clean session flag.
                Defaults to 3.
            properties (Properties | None, optional): Additional MQTT properties.
                Defaults to None.
            username (str | None, optional): Username for authentication.
                Defaults to None.
            password (str | None, optional): Password for authentication.
                Defaults to None.

        Returns:
            MQTTErrorCode: The result of the connection attempt.
        """
        logger.debug(f"[sync] Connecting to '{hostname}:{port}'")
        if username is not None:
            self._client.username = username

        if password is not None:
            self._client.password = password

        return self._client.connect(
            hostname,
            port,
            keepalive,
            bind_address,
            bind_port,
            clean_start,
            properties,
        )

    def publish_sync(
        self,
        topic: str,
        payload: str | bytes | bytearray | int | float | Json | None = None,
        qos: int = 0,
        retain: bool = False,
        properties: Properties | None = None,
    ):
        """
        Publishes a message to a topic synchronously.

        Args:
            topic (str): The topic to publish to.
            payload (Union[str, bytes, bytearray, int, float, Json, None], optional):
                The message payload. Defaults to None.
            qos (int, optional): The QoS level for the publication. Defaults to 0.
            retain (bool, optional): Whether to retain the message. Defaults to False.
            properties (Properties | None, optional): Additional MQTT properties.
                Defaults to None.

        Returns:
            MQTTErrorCode: The result of the publish attempt.
        """
        logger.debug(f"[sync] Publishing message to '{topic}'")
        if is_json(payload):
            payload = json.dumps(payload)
        return self._client.publish(topic, payload, qos, retain, properties)

    def reconnect_sync(self):
        """
        Reconnects the MQTT client to the broker synchronously.

        Returns:
            MQTTErrorCode: The result of the reconnection attempt.
        """
        logger.debug("[sync] Reconnect")
        return self._client.reconnect()

    def __on_paho_connect_event(
        self,
        client: PahoClient,
        userdata: Any,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Internal handler for Paho MQTT connection events.

        Args:
            client (PahoClient): The MQTT client instance.
            userdata (Any): User-defined data passed to the callback.
            flags (ConnectFlags): Connection flags.
            reason_code (ReasonCode): The reason code for the connection.
            properties (Properties | None): Additional MQTT properties.
        """
        event = OnConnectEvent.from_paho_event(self, flags, reason_code, properties)
        self._handle_on_connect(event)
        for topic, qos in self._pending_subscriptions:
            self.subscribe_sync(topic, qos)

        self._pending_subscriptions.clear()

    def __on_paho_disconnect_event(
        self,
        client: PahoClient,
        userdata: Any,
        flags: DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Internal handler for Paho MQTT disconnection events.

        Args:
            client (PahoClient): The MQTT client instance.
            userdata (Any): User-defined data passed to the callback.
            flags (DisconnectFlags): Disconnection flags.
            reason_code (ReasonCode): The reason code for the disconnection.
            properties (Properties | None): Additional MQTT properties.
        """
        event = OnDisconnectEvent.from_paho_event(self, flags, reason_code, properties)
        self._handle_on_disconnect(event)

    def __on_paho_message_event(
        self,
        client: PahoClient,
        userdata: Any,
        message: MQTTMessage,
    ):
        """
        Internal handler for Paho MQTT message events.

        Args:
            client (PahoClient): The MQTT client instance.
            userdata (Any): User-defined data passed to the callback.
            message (MQTTMessage): The received MQTT message.
        """
        event = OnMessageEvent.from_paho_event(self, message)
        self._handle_on_message(event)

    @abstractmethod
    def _handle_on_connect(self, event: OnConnectEvent): ...

    @abstractmethod
    def _handle_on_disconnect(self, event: OnDisconnectEvent): ...

    @abstractmethod
    def _handle_on_message(self, event: OnMessageEvent): ...


class AbstractSimpleMqttAsync(AbstractSimpleMqtt):
    """
    Abstract class for managing asynchronous MQTT clients using Paho MQTT.

    This class provides asynchronous wrappers and utilities for handling MQTT
    connections, message subscriptions, and publishing messages.
    """

    _loop: asyncio.AbstractEventLoop
    _connected_event: asyncio.Event
    _socket_ready_event: asyncio.Event

    def __init__(self, *, loop: Optional[asyncio.AbstractEventLoop] = None):
        """
        Initializes the AbstractSimpleMqttAsync instance.

        Args:
            loop (Optional[asyncio.AbstractEventLoop]): The asyncio event loop to use.
                If None, the current running loop is used.
        """
        super().__init__()
        self._loop = loop or asyncio.get_running_loop()
        self._connected_event = asyncio.Event()
        self._socket_ready_event = asyncio.Event()
        self._client.on_socket_open = self._handle_on_socket_open
        self._client.on_socket_close = self._handle_on_socket_close

    def _handle_on_socket_open(
        self, client: PahoClient, userdata: Any, socket: SocketLike
    ):
        """
        Handles the event when the MQTT socket is opened.

        Args:
            client (PahoClient): The MQTT client instance.
            userdata (Any): User-defined data passed to the callback.
            socket (SocketLike): The opened socket.
        """
        self._loop.call_soon_threadsafe(self._socket_ready_event.set)
        logger.debug("[async] Socket opened")

    def _handle_on_socket_close(
        self, client: PahoClient, userdata: Any, socket: SocketLike
    ):
        """
        Handles the event when the MQTT socket is closed.

        Args:
            client (PahoClient): The MQTT client instance.
            userdata (Any): User-defined data passed to the callback.
            socket (SocketLike): The closed socket.
        """
        self._loop.call_soon_threadsafe(self._socket_ready_event.clear)
        logger.debug("[async] Socket closed")

    def _handle_connected_event(self, cond: bool) -> Self:
        """
        Updates the connected event state based on the connection condition.

        Args:
            cond (bool): True if the client is connected, False otherwise.

        Returns:
            Self: The current instance for method chaining.
        """
        if cond:
            self._loop.call_soon_threadsafe(self._connected_event.set)
            logger.debug("[async] Connected")
        else:
            self._loop.call_soon_threadsafe(self._connected_event.clear)
            logger.error("[async] Connection failed")
        return self

    async def publish_async(
        self,
        topic: str,
        payload: str | bytes | bytearray | int | float | Json | None = None,
        qos: int = 0,
        retain: bool = False,
        properties: Properties | None = None,
    ):
        """
        Publishes a message to a topic asynchronously.

        Args:
            topic (str): The topic to publish to.
            payload (Union[str, bytes, bytearray, int, float, Json, None], optional):
                The message payload. Defaults to None.
            qos (int, optional): The QoS level for the publication. Defaults to 0.
            retain (bool, optional): Whether to retain the message. Defaults to False.
            properties (Properties | None, optional): Additional MQTT properties.
                Defaults to None.

        Returns:
            Any: The result of the publish attempt.
        """
        logger.debug(f"[async] Publishing message to '{topic}'")
        return self._loop.run_in_executor(
            None, self.publish_sync, topic, payload, qos, retain, properties
        )

    async def subscribe_async(self, topic: str, qos: int = 0):
        """
        Subscribes to a topic asynchronously.

        Args:
            topic (str): The topic to subscribe to.
            qos (int, optional): The QoS level for the subscription. Defaults to 0.

        Returns:
            Any: The result of the subscription attempt.
        """
        logger.debug(f"[async] Subscribing to '{topic}' with QoS {qos}")
        return self._loop.run_in_executor(None, self.subscribe_sync, topic, qos)

    async def wait_for_connection(self, timeout: float | None = None) -> None:
        """
        Waits for the MQTT client to establish a connection.

        Args:
            timeout (float | None, optional): The maximum time to wait in seconds.
                Defaults to None.

        Raises:
            asyncio.TimeoutError: If the connection is not established within the
                timeout period.
        """
        await asyncio.wait_for(self._connected_event.wait(), timeout)

    async def connect_async(
        self,
        hostname: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
        bind_port: int = 0,
        clean_start: bool | Literal[3] = 3,
        properties: Properties | None = None,
        *,
        username: str | None = None,
        password: str | None = None,
    ):
        """
        Connects to an MQTT broker asynchronously.

        Args:
            hostname (str): The broker hostname.
            port (int, optional): The broker port. Defaults to 1883.
            keepalive (int, optional): Keepalive interval in seconds. Defaults to 60.
            bind_address (str, optional): Local bind address. Defaults to "".
            bind_port (int, optional): Local bind port. Defaults to 0.
            clean_start (bool | Literal[3], optional): Clean session flag.
                Defaults to 3.
            properties (Properties | None, optional): Additional MQTT properties.
                Defaults to None.
            username (str | None, optional): Username for authentication.
                Defaults to None.
            password (str | None, optional): Password for authentication.
                Defaults to None.

        Returns:
            Any: The result of the connection attempt.
        """
        logger.debug(f"[async] Connecting to '{hostname}:{port}'")
        return self._loop.run_in_executor(
            None,
            functools.partial(
                self.connect_sync,
                hostname,
                port,
                keepalive,
                bind_address,
                bind_port,
                clean_start,
                properties,
                username=username,
                password=password,
            ),
        )

    def _handle_read(self):
        """
        Handles incoming data from the MQTT client socket.
        """
        self._client.loop_read()

    def _hanlde_write(self):
        """
        Handles outgoing data to the MQTT client socket.
        """
        self._client.loop_write()

    async def _handle_misc(self):
        """
        Handles miscellaneous network events for the MQTT client.

        Runs in a loop to process periodic tasks like pings.
        """
        while self.started:
            self._client.loop_misc()
            await asyncio.sleep(0.01)

    async def start_async(self):
        """
        Starts the MQTT client and initializes its connection.

        Raises:
            RuntimeError: If the client fails to start due to missing socket.
        """
        if self.started:
            logger.warning("[async] Connection already started. Call ignored.")
            return

        logger.debug("[async] Starting MQTT client")

        await asyncio.wait_for(self._socket_ready_event.wait(), timeout=10)
        sock = self._client.socket()
        if sock is None:
            logger.error("[async] No socket available. Cannot start.")
            # TODO handle error
            return

        self._loop.add_reader(sock, self._handle_read)
        self._loop.add_writer(sock, self._hanlde_write)

        self._started = True

        self._loop.create_task(self._handle_misc())

    async def stop_async(self):
        """
        Stops the MQTT client and releases its resources.

        Raises:
            RuntimeError: If the client fails to stop due to missing socket.
        """
        if not self.started:
            logger.warning("[async] Connection already stopped. Call ignored.")
            return

        logger.debug("[async] Stopping MQTT client")

        sock = self._client.socket()

        if sock is not None:
            self._loop.remove_reader(sock)
            self._loop.remove_writer(sock)
        else:
            logger.error("[async] No socket available. Cannot stop.")
            # TODO handle error

        self._started = False
