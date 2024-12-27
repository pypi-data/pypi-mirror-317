from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import TypeAlias, Self

from .DualContextCallback import DualContextCallback
from .EventData import OnMessageEvent
from .utils import is_pattern_topic, topic_matches_pattern

if TYPE_CHECKING:
    from .DualContextCallback import DualContextCallbackType

CallbackDict: TypeAlias = dict[str, DualContextCallback[OnMessageEvent]]


class TopicsMessageCallback:
    """
    A class for managing message callbacks associated with MQTT topics.

    This class handles callbacks for both strict topics and wildcard patterns,
    enabling efficient handling of messages based on topic matching.
    """

    __strict: CallbackDict
    __wildcard: CallbackDict

    def __init__(self) -> None:
        """
        Initializes the TopicsMessageCallback instance.

        Sets up separate dictionaries for strict topics and wildcard patterns.
        """

        self.__strict = {}
        self.__wildcard = {}

    def _add_strict(
        self, topic: str, callback: DualContextCallbackType[OnMessageEvent]
    ) -> None:
        """
        Adds a callback for a strict topic.

        Args:
            topic (str): The exact topic for which the callback is registered.
            callback (DualContextCallbackType[OnMessageEvent]): The callback to add.
        """

        if topic not in self.__strict:
            self.__strict[topic] = DualContextCallback()
        self.__strict[topic].add(callback)

    def _add_wildcard(
        self, topic: str, callback: DualContextCallbackType[OnMessageEvent]
    ) -> None:
        """
        Adds a callback for a wildcard topic pattern.

        Args:
            topic (str): The wildcard topic pattern.
            callback (DualContextCallbackType[OnMessageEvent]): The callback to add.
        """
        if topic not in self.__wildcard:
            self.__wildcard[topic] = DualContextCallback()
        self.__wildcard[topic].add(callback)

    def add(
        self, topic: str, callback: DualContextCallbackType[OnMessageEvent]
    ) -> Self:
        """
        Adds a callback for a topic, determining whether it is strict or a wildcard
        pattern.

        Args:
            topic (str): The topic or pattern to register.
            callback (DualContextCallbackType[OnMessageEvent]): The callback to add.

        Returns:
            Self: The instance of the class for method chaining.
        """

        if is_pattern_topic(topic):
            self._add_wildcard(topic, callback)
        else:
            self._add_strict(topic, callback)
        return self

    @property
    def strict_topics(self) -> list[str]:
        """
        Retrieves the list of strict topics.

        Returns:
            list[str]: A list of strict topic names.
        """
        return list(self.__strict.keys())

    @property
    def wilcard_topics(self) -> list[str]:
        """
        Retrieves the list of wildcard topics.

        Returns:
            list[str]: A list of wildcard topic patterns.
        """
        return list(self.__wildcard.keys())

    @property
    def topics(self) -> list[str]:
        """
        Retrieves the combined list of all topics (strict and wildcard).

        Returns:
            list[str]: A list of all topic names and patterns.
        """
        return self.strict_topics + self.wilcard_topics

    def call_sync(self, event: OnMessageEvent) -> None:
        """
        Calls all registered callbacks for a given event in a synchronous context.

        This method is intended for use in synchronous code and will execute
        asynchronous callbacks in a blocking manner.

        Args:
            event (OnMessageEvent): The event containing the topic and message payload.
        """
        topic = event.topic
        if topic in self.__strict:
            self.__strict[topic].call_sync(event)

        for pattern in self.wilcard_topics:
            if topic_matches_pattern(topic, pattern):
                self.__wildcard[pattern].call_sync(event)

    async def call_async(self, event: OnMessageEvent) -> None:
        """
        Calls all registered callbacks for a given event in an asynchronous context.

        This method is intended for use in asynchronous code and will execute
        synchronous callbacks in a non-blocking manner using asyncio.

        Args:
            event (OnMessageEvent): The event containing the topic and message payload.
        """
        topic = event.topic
        if topic in self.__strict:
            await self.__strict[topic].call_async(event)

        for pattern in self.wilcard_topics:
            if topic_matches_pattern(topic, pattern):
                await self.__wildcard[pattern].call_async(event)
