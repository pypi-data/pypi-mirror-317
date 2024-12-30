from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QHBoxLayout

from .TopicsList import TopicsList
from .TopicLog import TopicLog

if TYPE_CHECKING:
    pass


class ViewerPage(QWidget):
    """
    Represents the main viewer page for displaying MQTT topics and their logs.

    Attributes:
        root_layout: The horizontal layout that contains the topics list and topic log
        widgets.
        topics_list: The widget displaying the list of MQTT topics.
        topic_log: The widget displaying the logs for a selected topic.
    """

    root_layout: QHBoxLayout

    topics_list: TopicsList
    topic_log: TopicLog

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initialize the ViewerPage widget.

        :param parent: The parent widget, if any.
        """
        super().__init__(parent)
        self.build()

    def build(self):
        """
        Build the UI for the ViewerPage, adding the topics list and topic log widgets.
        """
        self.root_layout = QHBoxLayout(self)

        self.topics_list = TopicsList(self)
        self.topic_log = TopicLog(self)
        self.root_layout.addWidget(self.topics_list, 1)
        self.root_layout.addWidget(self.topic_log, 3)

        self.setLayout(self.root_layout)
