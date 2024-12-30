from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Optional, Literal, TypeAlias, Self
from datetime import datetime
import json

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from ki2_python_utils import Json, is_json, exist

from .SignalManager import get_signal_manager

if TYPE_CHECKING:
    from paho.mqtt.reasoncodes import ReasonCode
    from paho.mqtt.properties import Properties

SourceType: TypeAlias = Literal["received", "send"]


class MessageItem:
    """
    Represents a single MQTT message with metadata including timestamp, payload, and
    source.
    """

    _timestamp: datetime
    _payload: bytes
    _source: SourceType

    def __init__(
        self, payload: bytes, source: SourceType, timestamp: Optional[datetime] = None
    ) -> None:
        """
        Initialize a MessageItem instance.

        :param payload: The message payload as bytes.
        :param source: The source of the message ("received" or "send").
        :param timestamp: The timestamp of the message, defaults to the current time.
        """
        self._timestamp = timestamp or datetime.now()
        self._payload = payload
        self._source = source

    @property
    def timestamp(self) -> datetime:
        """
        Get the timestamp of the message.

        :return: The timestamp as a datetime object.
        """
        return self._timestamp

    @property
    def payload(self) -> bytes:
        """
        Get the payload of the message.

        :return: The payload as bytes.
        """
        return self._payload

    @property
    def source(self) -> SourceType:
        """
        Get the source of the message.

        :return: The source as a string ("received" or "send").
        """
        return self._source

    @property
    def as_string(self) -> str:
        """
        Get the payload as a UTF-8 string.

        :return: The payload as a decoded string.
        """
        return self._payload.decode("utf-8")


class MqttHandler:
    """
    Handles MQTT communication, including connecting, publishing, and receiving
    messages.
    """

    client: mqtt.Client

    _mqtt_address: str = "localhost"
    _mqtt_port: int = 1883
    _mqtt_username: str | None = None
    _mqtt_password: str | None = None

    messages: dict[str, list[MessageItem]] = {}
    _max_messages: int | None

    def __init__(self, max_messages: int | None = None) -> None:
        """
        Initialize the MQTT handler.

        :param max_messages: Maximum number of messages to store per topic.
        """
        self._max_messages = max_messages
        self.client = mqtt.Client(CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.on_disconnect = self.__on_disconnect

    @property
    def max_messages(self) -> int | None:
        """
        Get the maximum number of messages stored per topic.

        :return: The maximum number of messages or None if unlimited.
        """
        return self._max_messages

    @property
    def topics(self) -> list[str]:
        """
        Get the list of topics with stored messages.

        :return: A list of topic names.
        """
        return list(self.messages.keys())

    @max_messages.setter
    def max_messages(self, value: int | None) -> None:
        """
        Set the maximum number of messages to store per topic.

        :param value: The maximum number of messages or None for unlimited.
        """
        if isinstance(value, int) and value < 1:
            value = None
        self._max_messages = value

    def __on_connect(
        self,
        client: mqtt.Client,
        userdata: None,
        flags: mqtt.ConnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Callback triggered when the client connects to the broker.

        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param flags: Response flags sent by the broker.
        :param reason_code: Reason code for the connection result.
        :param properties: MQTT v5 properties.
        """
        self.client.subscribe("#")

    def __on_disconnect(
        self,
        client: mqtt.Client,
        userdata: None,
        flags: mqtt.DisconnectFlags,
        reason_code: ReasonCode,
        properties: Properties | None,
    ):
        """
        Callback triggered when the client disconnects from the broker.

        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param flags: Disconnect flags sent by the broker.
        :param reason_code: Reason code for the disconnection.
        :param properties: MQTT v5 properties.
        """
        self.client.unsubscribe("#")

    def __on_message(
        self,
        client: mqtt.Client,
        userdata: None,
        message: mqtt.MQTTMessage,
    ):
        """
        Callback triggered when a message is received from the broker.

        :param client: The MQTT client instance.
        :param userdata: User-defined data of any type.
        :param message: The received MQTT message.
        """
        self.add_message(
            topic=message.topic,
            payload=message.payload,
            source="received",
            timestamp=datetime.now(),
        )

    def add_message(
        self,
        topic: str,
        payload: bytes,
        source: SourceType,
        timestamp: Optional[datetime] = None,
    ):
        """
        Add a message to the internal storage for a topic.

        :param topic: The topic of the message.
        :param payload: The message payload as bytes.
        :param source: The source of the message ("received" or "send").
        :param timestamp: The timestamp of the message, defaults to the current time.
        """
        message = MessageItem(
            payload=payload,
            source=source,
            timestamp=timestamp,
        )

        if topic not in self.messages:
            self.messages[topic] = []
            get_signal_manager().emit_new_topic(topic)

        self.messages[topic].append(message)

        if (
            self._max_messages is not None
            and len(self.messages[topic]) > self._max_messages
        ):
            self.messages[topic].pop(0)

        get_signal_manager().emit_new_message(topic, message)

    def connect_settings(
        self,
        address: Optional[str] = None,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Configure the connection settings for the MQTT client.

        :param address: The broker address.
        :param port: The broker port.
        :param username: The username for authentication.
        :param password: The password for authentication.
        """
        if exist(address):
            self._mqtt_address = address
        if exist(port):
            self._mqtt_port = port
        if exist(username):
            self._mqtt_username = username
        if exist(password):
            self._mqtt_password = password

    def publish(self, topic: str, payload: bytes | str | Json):
        """
        Publish a message to a specific topic.

        :param topic: The topic to publish to.
        :param payload: The message payload as bytes, string, or JSON.
        """
        if is_json(payload):
            payload = json.dumps(payload).encode("utf-8")
        elif isinstance(payload, str):
            payload = payload.encode("utf-8")
        self.client.publish(topic, payload)
        self.add_message(topic, payload, "send")

    def connect(
        self,
    ) -> Self:
        """
        Connect to the MQTT broker using the configured settings.

        :return: The current instance of MqttHandler.
        """
        self.client.connect(self._mqtt_address, self._mqtt_port)
        if exist(self._mqtt_username) and exist(self._mqtt_password):
            self.client.username_pw_set(self._mqtt_username, self._mqtt_password)
        self.client.loop_start()
        return self

    def get_messages(self, topic: str) -> list[MessageItem]:
        """
        Retrieve the messages for a specific topic.

        :param topic: The topic to retrieve messages for.
        :return: A list of MessageItem objects.
        """
        return self.messages.get(topic, [])


_mqtt_handler: MqttHandler | None = None


def get_mqtt_handler() -> MqttHandler:
    """
    Get the singleton instance of MqttHandler.

    :return: The singleton instance of MqttHandler.
    """
    global _mqtt_handler
    if _mqtt_handler is None:
        _mqtt_handler = MqttHandler()
    return _mqtt_handler
