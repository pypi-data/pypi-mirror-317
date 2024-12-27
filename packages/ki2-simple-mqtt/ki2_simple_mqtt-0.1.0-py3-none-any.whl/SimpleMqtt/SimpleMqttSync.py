from __future__ import annotations
from typing import TYPE_CHECKING

from .AbstractSimpleMqtt import AbstractSimpleMqtt
from .EventData import OnConnectEvent, OnDisconnectEvent, OnMessageEvent

if TYPE_CHECKING:
    from ki2_python_utils import Json


class SimpleMqttSync(AbstractSimpleMqtt):
    """
    Synchronous implementation of the AbstractSimpleMqtt class.

    This class provides synchronous methods for connecting, subscribing, and
    publishing messages using the MQTT protocol.
    """

    def __init__(self):
        """
        Initializes the SimpleMqttSync instance.
        """
        super().__init__()

    def _handle_on_connect(self, event: OnConnectEvent):
        """
        Handles the on_connect event in a synchronous context.

        Args:
            event (OnConnectEvent): The connection event data.
        """
        self._on_connect.call_sync(event)

    def _handle_on_disconnect(self, event: OnDisconnectEvent):
        """
        Handles the on_disconnect event in a synchronous context.

        Args:
            event (OnDisconnectEvent): The disconnection event data.
        """
        self._on_disconnect.call_sync(event)

    def _handle_on_message(self, event: OnMessageEvent):
        """
        Handles the on_message event in a synchronous context.

        Args:
            event (OnMessageEvent): The message event data.
        """
        self._on_message.call_sync(event)
        self._on_topic_message.call_sync(event)

    def publish(self, topic: str, payload: str | Json):
        """
        Publishes a message to a topic synchronously.

        Args:
            topic (str): The topic to publish to.
            payload (str | Json): The message payload.
        """
        self.publish_sync(topic, payload)

    def subscribe(self, topic: str, qos: int = 0):
        """
        Subscribes to a topic synchronously.

        Args:
            topic (str): The topic to subscribe to.
            qos (int, optional): The QoS level for the subscription. Defaults to 0.

        Returns:
            Any: The result of the subscription attempt.
        """
        return self.subscribe_sync(topic, qos)

    def connect(
        self,
        hostname: str,
        port: int = 1883,
        keepalive: int = 60,
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
            username (str | None, optional): Username for authentication.
                Defaults to None.
            password (str | None, optional): Password for authentication.
                Defaults to None.

        Returns:
            Any: The result of the connection attempt.
        """
        return self.connect_sync(
            hostname,
            port,
            keepalive,
            username=username,
            password=password,
        )

    def reconnect(self):
        """
        Reconnects to the MQTT broker synchronously.

        Returns:
            Any: The result of the reconnection attempt.
        """
        return self.reconnect_sync()

    def loop_start(self):
        """
        Starts the MQTT network loop in a separate thread.
        """
        return self._client.loop_start()

    def loop_stop(self):
        """
        Stops the MQTT network loop that was started in a separate thread.
        """
        return self._client.loop_stop()

    def loop_forever(self, timeout: float = 1.0, retry_first_connection: bool = False):
        """
        Blocks and processes MQTT network events indefinitely.

        Args:
            timeout (float, optional): The timeout for the network loop in seconds.
                Defaults to 1.0.
            retry_first_connection (bool, optional): Whether to retry the first
                connection. Defaults to False.
        """
        return self._client.loop_forever(timeout, retry_first_connection)
