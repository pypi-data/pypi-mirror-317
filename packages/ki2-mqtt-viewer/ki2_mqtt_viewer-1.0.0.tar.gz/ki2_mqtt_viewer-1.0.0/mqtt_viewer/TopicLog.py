from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QSizePolicy
from PySide6.QtCore import Signal
from PySide6.QtGui import QResizeEvent

from .MqttHandler import get_mqtt_handler, MessageItem
from .SignalManager import get_signal_manager

if TYPE_CHECKING:
    pass


class TopicLog(QWidget):
    """
    A widget for displaying and sending messages for a selected MQTT topic.

    Attributes:
        selected_topic: The currently selected topic for logging and messaging.
        root_layout: The main layout of the widget.
        message_log: A text edit widget for displaying the message log.
        message_input: A text edit widget for composing new messages.
        send_message_button: A button to send composed messages.
        new_message_signal: A signal emitted when a new message is received.
        selected_topic_signal: A signal emitted when the selected topic changes.
    """

    selected_topic: str | None = None

    root_layout: QVBoxLayout
    message_log: QTextEdit
    message_input: QTextEdit
    send_message_button: QPushButton

    new_message_signal = Signal(str, MessageItem)
    selected_topic_signal = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialize the TopicLog widget and set up the UI and signal connections.

        :param parent: The parent widget, if any.
        """

        super().__init__(parent)
        self.build()
        self.new_message_signal.connect(self.on_new_message)
        self.selected_topic_signal.connect(self.on_select_topic)
        signals = get_signal_manager()
        signals.set_select_topic_signal(self.selected_topic_signal)
        signals.set_new_message_signal(self.new_message_signal)

    def build(self):
        """
        Build the UI for the TopicLog widget.
        This includes setting up the message log, input, and send button.
        """

        self.root_layout = QVBoxLayout(self)

        self.message_log = QTextEdit(self)
        self.message_log.setReadOnly(True)
        self.root_layout.addWidget(self.message_log)

        self.message_input = QTextEdit(self)
        self.message_input.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.message_input.setMaximumHeight(30)
        self.message_input.textChanged.connect(self.__adjust_message_input_height)
        self.root_layout.addWidget(self.message_input)

        self.send_message_button = QPushButton("Send Message", self)
        self.send_message_button.clicked.connect(self.send_message)
        self.root_layout.addWidget(self.send_message_button)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Handle resize events to adjust the height of the message input field.

        :param event: The resize event.
        """
        self.__adjust_message_input_height()
        super().resizeEvent(event)

    def __adjust_message_input_height(self) -> None:
        """
        Adjust the height of the message input field based on its content.
        """
        document = self.message_input.document()
        document_height = document.size().height()
        self.message_input.setMaximumHeight(
            int(min(document_height + 2, self.height() * 0.25))
        )

    def append_message(self, message: MessageItem) -> None:
        """
        Append a message to the message log with timestamp and styling.

        :param message: The message to append.
        """
        timestamp: str = message.timestamp.isoformat()
        content: str = message.as_string

        color = "blue"
        if message.source == "send":
            color = "green"

        f_msg = f"<span style='color: {color};'>{timestamp}:</span> {content}"
        self.message_log.append(f_msg)

    def on_new_message(self, topic: str, message: MessageItem):
        """
        Handle the event of a new message received.
        Append the message if it belongs to the selected topic.

        :param topic: The topic of the message.
        :param message: The MessageItem object containing message details.
        """
        if topic != self.selected_topic:
            return
        self.append_message(message)

    def on_select_topic(self, topic: str):
        """
        Handle the event of a topic selection change.
        Update the log to display messages for the selected topic.

        :param topic: The newly selected topic.
        """
        if topic == self.selected_topic:
            return
        self.selected_topic = topic
        self.message_log.clear()
        messages = get_mqtt_handler().get_messages(self.selected_topic)
        for message in messages:
            self.append_message(message)

    def send_message(self) -> None:
        """
        Send a message to the selected topic.
        Publish the message via the MQTT handler and clear the input field.
        """
        if self.selected_topic is None:
            return

        message = self.message_input.toPlainText()
        if len(message) > 0:
            get_mqtt_handler().publish(self.selected_topic, message)
            self.message_input.clear()
