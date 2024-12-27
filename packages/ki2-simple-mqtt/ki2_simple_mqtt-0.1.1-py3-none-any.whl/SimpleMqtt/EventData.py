from __future__ import annotations
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .AbstractSimpleMqtt import AbstractSimpleMqtt
    from paho.mqtt.client import ConnectFlags, DisconnectFlags, MQTTMessage
    from paho.mqtt.reasoncodes import ReasonCode
    from paho.mqtt.properties import Properties
    from ki2_python_utils import Json


class BaseEvent:
    """
    Base class for all events in the MQTT client.

    Attributes:
        _client (AbstractSimpleMqtt): The MQTT client instance associated with the
            event.
    """

    _client: AbstractSimpleMqtt

    def __init__(self, client: AbstractSimpleMqtt):
        """
        Initializes the BaseEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance associated with the
                event.
        """
        self._client = client

    @property
    def client(self) -> AbstractSimpleMqtt:
        """
        The MQTT client instance associated with the event.

        Returns:
            AbstractSimpleMqtt: The MQTT client instance.
        """
        return self._client


class BaseConnectionEvent(BaseEvent):
    """
    Base class for connection-related events in the MQTT client.

    Attributes:
        _reason_code (ReasonCode): The reason code for the connection event.
        _properties (Properties | None): The properties associated with the event.
    """

    _reason_code: ReasonCode
    _properties: Properties | None

    def __init__(
        self,
        client: AbstractSimpleMqtt,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Initializes the BaseConnectionEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            reason_code (ReasonCode): The reason code for the connection event.
            properties (Properties | None): Additional properties associated with the
                event.
        """
        super().__init__(client)
        self._reason_code = reason_code
        self._properties = properties

    @property
    def reason_code(self) -> ReasonCode:
        """
        The reason code for the connection event.

        Returns:
            ReasonCode: The reason code.
        """
        return self._reason_code

    @property
    def properties(self) -> Properties | None:
        """
        Initializes the OnConnectEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            flags (ConnectFlags): Connection flags.
            reason_code (ReasonCode): The reason code for the connection.
            properties (Properties | None): Additional properties associated with the
            event.
        """
        return self._properties


class OnConnectEvent(BaseConnectionEvent):
    """
    Event triggered when the MQTT client connects to a broker.

    Attributes:
        _flags (ConnectFlags): Connection flags indicating the result of the connection.
    """

    _flags: ConnectFlags

    def __init__(
        self,
        client: AbstractSimpleMqtt,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Initializes the OnConnectEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            flags (ConnectFlags): Connection flags.
            reason_code (ReasonCode): The reason code for the connection.
            properties (Properties | None): Additional properties associated with the
                event.
        """
        super().__init__(client, reason_code, properties)
        self._flags = flags

    @property
    def flags(self) -> ConnectFlags:
        """
        The connection flags indicating the result of the connection.

        Returns:
            ConnectFlags: The connection flags.
        """
        return self._flags

    @staticmethod
    def from_paho_event(
        client: AbstractSimpleMqtt,
        flags: ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ) -> OnConnectEvent:
        """
        Creates an OnConnectEvent instance from Paho MQTT event parameters.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            flags (ConnectFlags): Connection flags.
            reason_code (ReasonCode): The reason code for the connection.
            properties (Properties | None): Additional properties associated with the
                event.

        Returns:
            OnConnectEvent: The created OnConnectEvent instance.
        """
        return OnConnectEvent(client, flags, reason_code, properties)


class OnDisconnectEvent(BaseConnectionEvent):
    """
    Event triggered when the MQTT client disconnects from a broker.

    Attributes:
        _flags (DisconnectFlags): Disconnection flags indicating the reason for the
            disconnection.
    """

    _flags: DisconnectFlags

    def __init__(
        self,
        client: AbstractSimpleMqtt,
        flags: DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Initializes the OnDisconnectEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            flags (DisconnectFlags): Disconnection flags.
            reason_code (ReasonCode): The reason code for the disconnection.
            properties (Properties | None): Additional properties associated with the
                event.
        """
        super().__init__(client, reason_code, properties)
        self._flags = flags

    @property
    def flags(self) -> DisconnectFlags:
        """
        The disconnection flags indicating the reason for the disconnection.

        Returns:
            DisconnectFlags: The disconnection flags.
        """
        return self._flags

    @staticmethod
    def from_paho_event(
        client: AbstractSimpleMqtt,
        flags: DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ) -> OnDisconnectEvent:
        """
        Creates an OnDisconnectEvent instance from Paho MQTT event parameters.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            flags (DisconnectFlags): Disconnection flags.
            reason_code (ReasonCode): The reason code for the disconnection.
            properties (Properties | None): Additional properties associated with the
                event.

        Returns:
            OnDisconnectEvent: The created OnDisconnectEvent instance.
        """
        return OnDisconnectEvent(client, flags, reason_code, properties)


class OnMessageEvent(BaseEvent):
    """
    Event triggered when an MQTT message is received.

    Attributes:
        _source_message (MQTTMessage): The original MQTT message.
    """

    _source_message: MQTTMessage

    def __init__(self, client: AbstractSimpleMqtt, source_message: MQTTMessage):
        """
        Initializes the OnMessageEvent.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            source_message (MQTTMessage): The original MQTT message.
        """
        super().__init__(client)
        self._source_message = source_message

    @property
    def client(self) -> AbstractSimpleMqtt:
        """
        The MQTT client instance associated with the message.

        Returns:
            AbstractSimpleMqtt: The MQTT client instance.
        """
        return self._client

    @property
    def source_message(self) -> MQTTMessage:
        """
        The original MQTT message.

        Returns:
            MQTTMessage: The original message.
        """
        return self._source_message

    @property
    def topic(self) -> str:
        """
        The topic of the received MQTT message.

        Returns:
            str: The topic name.
        """
        return self._source_message.topic

    @property
    def payload(self) -> bytes:
        """
        The payload of the received MQTT message.

        Returns:
            bytes: The payload data.
        """
        return self._source_message.payload

    @property
    def as_string(self) -> str:
        """
        The payload of the MQTT message decoded as a UTF-8 string.

        Returns:
            str: The decoded string.
        """
        return self._source_message.payload.decode("utf-8")

    @property
    def as_json(self) -> Json:
        """
        The payload of the MQTT message parsed as JSON.

        Returns:
            Json: The parsed JSON data.
        """
        return json.loads(self.payload)

    @staticmethod
    def from_paho_event(
        client: AbstractSimpleMqtt, source_message: MQTTMessage
    ) -> OnMessageEvent:
        """
        Creates an OnMessageEvent instance from Paho MQTT event parameters.

        Args:
            client (AbstractSimpleMqtt): The MQTT client instance.
            source_message (MQTTMessage): The original MQTT message.

        Returns:
            OnMessageEvent: The created OnMessageEvent instance.
        """
        return OnMessageEvent(client, source_message)
