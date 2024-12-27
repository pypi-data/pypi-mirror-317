from __future__ import annotations
from typing import TYPE_CHECKING
import asyncio
import logging

from paho.mqtt.client import CONNACK_ACCEPTED
from .AbstractSimpleMqtt import AbstractSimpleMqttAsync
from .EventData import OnConnectEvent, OnDisconnectEvent, OnMessageEvent

if TYPE_CHECKING:
    from ki2_python_utils import Json

logger = logging.getLogger(__name__)


class SimpleMqttAsync(AbstractSimpleMqttAsync):
    """
    Asynchronous implementation of the AbstractSimpleMqttAsync class.

    This class provides asynchronous methods for connecting, subscribing, and
    publishing messages using the MQTT protocol with asyncio.
    """

    _loop: asyncio.AbstractEventLoop
    _queue: asyncio.Queue[OnMessageEvent]

    def __init__(
        self,
        *,
        loop: asyncio.AbstractEventLoop | None = None,
    ):
        """
        Initializes the SimpleMqttAsync instance.

        Args:
            loop (asyncio.AbstractEventLoop | None): The event loop to use.
                If None, the current running loop will be used.
        """
        super().__init__(loop=loop)
        self._queue = asyncio.Queue()

    def _handle_on_connect(self, event: OnConnectEvent):
        """
        Handles the on_connect event in an asynchronous context.

        Args:
            event (OnConnectEvent): The connection event data.
        """
        self._loop.create_task(self._on_connect.call_async(event))
        self._handle_connected_event(event.reason_code == CONNACK_ACCEPTED)

    def _handle_on_disconnect(self, event: OnDisconnectEvent):
        """
        Handles the on_disconnect event in an asynchronous context.

        Args:
            event (OnDisconnectEvent): The disconnection event data.
        """
        self._loop.create_task(self._on_disconnect.call_async(event))

    def _handle_on_message(self, event: OnMessageEvent):
        """
        Handles the on_message event in an asynchronous context by queuing it.

        Args:
            event (OnMessageEvent): The message event data.
        """
        self._loop.call_soon_threadsafe(self._queue.put_nowait, event)

    async def _process_message(self):
        """
        Processes a single message from the event queue asynchronously.
        """
        event = await self._queue.get()
        await self._on_message.call_async(event)
        await self._on_topic_message.call_async(event)

    async def process_messages(self, max: int = 0):
        """
        Processes messages from the event queue asynchronously.

        Args:
            max (int, optional): The maximum number of messages to process.
                If 0, processes all available messages. Defaults to 0.
        """
        count = 0
        while max == 0 or count < max:
            if self._queue.empty():
                break
            await self._process_message()
            count += 1

    async def _handle_messages_queue(self, max: int = 100, sleep_time: float = 0.01):
        """
        Handles the message queue in a loop while the client is running.

        Args:
            max (int): Maximum number of messages to process per iteration.
            sleep_time (float): Time to sleep between iterations in seconds.
        """

        while self.started:
            await self.process_messages(max)
            await asyncio.sleep(sleep_time)

    async def publish(
        self,
        topic: str,
        payload: str | Json,
    ):
        """
        Publishes a message to a topic asynchronously.

        Args:
            topic (str): The topic to publish to.
            payload (str | Json): The message payload.

        Returns:
            Any: The result of the publish operation.
        """
        return await self.publish_async(topic, payload)

    async def subscribe(self, topic: str, qos: int = 0):
        """
        Subscribes to a topic asynchronously.

        Args:
            topic (str): The topic to subscribe to.
            qos (int, optional): The QoS level for the subscription. Defaults to 0.

        Returns:
            Any: The result of the subscription operation.
        """
        return await self.subscribe_async(topic, qos)

    async def connect(
        self,
        hostname: str,
        port: int = 1883,
        keepalive: int = 60,
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
            username (str | None, optional): Username for authentication.
                Defaults to None.
            password (str | None, optional): Password for authentication.
                Defaults to None.

        Returns:
            Any: The result of the connection attempt.
        """
        return await self.connect_async(
            hostname,
            port,
            keepalive,
            username=username,
            password=password,
        )

    async def disconnect(self):
        """
        Disconnects from the MQTT broker asynchronously.
        """
        await self._loop.run_in_executor(None, self._client.disconnect)

    async def start(self, max_message: int = 100, message_sleep: float = 0.01):
        """
        Starts the MQTT client and begins processing messages asynchronously.

        Args:
            max_message (int, optional): Maximum number of messages to process
                per iteration. Defaults to 100.
            message_sleep (float, optional): Time to sleep between message
                processing iterations in seconds. Defaults to 0.01.
        """
        if self.started:
            logger.warning("Already started")
            return

        await self.start_async()
        self._loop.create_task(self._handle_messages_queue(max_message, message_sleep))

    async def stop(self):
        """
        Stops the MQTT client and halts message processing asynchronously.
        """
        if not self.started:
            logger.warning("Already stopped")
            return

        await self.stop_async()

    async def loop(
        self,
        max_message: int = 100,
        message_sleep: float = 0.01,
        loop_sleep: float = 0.1,
    ):
        """
        Runs the MQTT client in an asynchronous loop.

        Args:
            max_message (int, optional): Maximum number of messages to process
                per iteration. Defaults to 100.
            message_sleep (float, optional): Time to sleep between message
                processing iterations in seconds. Defaults to 0.01.
            loop_sleep (float, optional): Time to sleep between loop iterations
                in seconds. Defaults to 0.1.
        """
        if self.started:
            logger.warning("Already started (in loop)")
            return

        await self.start(max_message, message_sleep)
        while self.started:
            await asyncio.sleep(loop_sleep)
        await self.stop()
