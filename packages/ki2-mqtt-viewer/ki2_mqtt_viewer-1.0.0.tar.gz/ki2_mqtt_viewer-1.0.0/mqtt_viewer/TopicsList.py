from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QInputDialog,
)

from PySide6.QtCore import Signal

from .MqttHandler import get_mqtt_handler
from .SignalManager import get_signal_manager

if TYPE_CHECKING:
    pass


class TopicsList(QWidget):
    """
    A widget that displays a list of MQTT topics and allows users to add and select
    topics.

    Attributes:
        root_layout: The main vertical layout of the widget.
        topics_list: A list widget to display the available topics.
        add_topic_button: A button to add new topics manually.
        new_topic_signal: A signal emitted when a new topic is detected.
    """

    root_layout: QVBoxLayout
    topics_list: QListWidget
    add_topic_button: QPushButton

    new_topic_signal = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialize the TopicsList widget and set up the UI and signal connections.

        :param parent: The parent widget, if any.
        """
        super().__init__(parent)
        self.build()
        self.new_topic_signal.connect(self.on_new_topic_detected)
        get_signal_manager().set_new_topic_signal(self.new_topic_signal)

        for topic in get_mqtt_handler().topics:
            self.add_topic(topic)

    def build(self):
        """
        Build the UI for the TopicsList widget.
        This includes setting up the layout, the list widget, and the add topic button.
        """
        self.root_layout = QVBoxLayout(self)
        self.topics_list = QListWidget(self)
        self.topics_list.clicked.connect(self.on_topic_selected)
        self.root_layout.addWidget(self.topics_list)

        self.add_topic_button = QPushButton("Add Topic", self)
        self.add_topic_button.clicked.connect(self.on_add_topic_button_clicked)
        self.root_layout.addWidget(self.add_topic_button)

    @property
    def topics(self) -> list[str]:
        """
        Get the list of topics currently displayed in the list widget.

        :return: A list of topic strings.
        """
        return [
            self.topics_list.item(i).text() for i in range(self.topics_list.count())
        ]

    @property
    def selected_topic(self) -> str | None:
        """
        Get the currently selected topic in the list widget.

        :return: The selected topic as a string, or None if no topic is selected.
        """
        current_item = self.topics_list.currentItem()
        return current_item.text() if current_item else None

    def add_topic(self, topic: str):
        """
        Add a new topic to the list widget if it is not already present.

        :param topic: The topic to add.
        """
        if len(topic) < 1:
            return
        if topic not in self.topics:
            self.topics_list.addItem(topic)
            if self.topics_list.count() == 1:
                self.topics_list.setCurrentRow(0)
                self.on_topic_selected()

    def on_topic_selected(self):
        """
        Handle the event when a topic is selected in the list widget.
        Emit a signal with the selected topic.
        """
        current_item = self.topics_list.currentItem()
        if current_item:
            get_signal_manager().emit_select_topic(current_item.text())

    def on_add_topic_button_clicked(self):
        """
        Handle the event when the "Add Topic" button is clicked.
        Open a dialog to input a new topic and add it to the list if confirmed.
        """
        new_topic, ok = QInputDialog.getText(self, "Add Topic", "Enter new topic:")
        if ok:
            self.add_topic(new_topic)

    def on_new_topic_detected(self, topic: str):
        """
        Handle the event when a new topic is detected.
        Add the topic to the list.

        :param topic: The newly detected topic.
        """
        self.add_topic(topic)
