from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import Self

from PySide6.QtCore import SignalInstance

if TYPE_CHECKING:
    from .MqttHandler import MessageItem


class SignalManager:
    """
    Manages Qt signals for communication between different components of the
    application.
    """

    _select_topic: SignalInstance | None = None
    _new_message: SignalInstance | None = None
    _new_topic: SignalInstance | None = None
    _connected: SignalInstance | None = None

    def __init__(self) -> None:
        """
        Initialize the SignalManager instance.
        """
        pass

    def set_select_topic_signal(self, signal: SignalInstance) -> Self:
        """
        Set the signal for topic selection.

        :param signal: The SignalInstance to be set for topic selection.
        :return: The current instance of SignalManager.
        """
        self._select_topic = signal
        return self

    def set_new_message_signal(self, signal: SignalInstance) -> Self:
        """
        Set the signal for new messages.

        :param signal: The SignalInstance to be set for new messages.
        :return: The current instance of SignalManager.
        """
        self._new_message = signal
        return self

    def set_new_topic_signal(self, signal: SignalInstance) -> Self:
        """
        Set the signal for new topics.

        :param signal: The SignalInstance to be set for new topics.
        :return: The current instance of SignalManager.
        """
        self._new_topic = signal
        return self

    def set_connected_signal(self, signal: SignalInstance) -> Self:
        """
        Set the signal for connection events.

        :param signal: The SignalInstance to be set for connection events.
        :return: The current instance of SignalManager.
        """
        self._connected = signal
        return self

    def emit_select_topic(self, topic: str) -> None:
        """
        Emit the select topic signal.

        :param topic: The topic to be emitted.
        """
        if self._select_topic is not None:
            self._select_topic.emit(topic)

    def emit_new_message(self, topic: str, message: MessageItem):
        """
        Emit the new message signal.

        :param topic: The topic associated with the message.
        :param message: The MessageItem instance containing message details.
        """
        if self._new_message is not None:
            self._new_message.emit(topic, message)

    def emit_new_topic(self, topic: str):
        """
        Emit the new topic signal.

        :param topic: The topic to be emitted.
        """
        if self._new_topic is not None:
            self._new_topic.emit(topic)

    def emit_connected(self):
        """
        Emit the connected signal.
        """
        if self._connected is not None:
            self._connected.emit()


_signal_manager: SignalManager | None = None


def get_signal_manager() -> SignalManager:
    """
    Get the singleton instance of SignalManager.

    :return: The singleton instance of SignalManager.
    """
    global _signal_manager
    if _signal_manager is None:
        _signal_manager = SignalManager()
    return _signal_manager
