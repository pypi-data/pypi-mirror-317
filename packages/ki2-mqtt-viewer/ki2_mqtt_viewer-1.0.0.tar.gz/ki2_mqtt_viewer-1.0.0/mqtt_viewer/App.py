from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMainWindow, QStackedWidget
from PySide6.QtCore import Signal

from .ViewerPage import ViewerPage
from .ConnectionPage import ConnectionPage

from .SignalManager import get_signal_manager

if TYPE_CHECKING:
    pass


class App(QMainWindow):
    """
    Main application window that manages the connection and viewer pages.

    Attributes:
        root: The main QStackedWidget managing the pages.
        viewer: The ViewerPage instance for displaying MQTT topics and logs.
        connection: The ConnectionPage instance for connecting to the MQTT broker.
        connected: A signal emitted when the MQTT client successfully connects.
    """

    root: QStackedWidget
    viewer: ViewerPage
    connection: ConnectionPage

    connected = Signal()

    def __init__(self) -> None:
        """
        Initialize the App instance and set up the UI and signal connections.
        """
        super().__init__()
        self.build()
        self.connected.connect(self.on_mqtt_connect)
        get_signal_manager().set_connected_signal(self.connected)

    def build(self):
        """
        Build the UI for the main application window.
        Set up the stacked widget and add the connection and viewer pages.
        """
        self.setWindowTitle("MQTT Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.root = QStackedWidget(self)
        self.setCentralWidget(self.root)

        self.viewer = ViewerPage(self)
        self.connection = ConnectionPage(self)

        self.root.addWidget(self.connection)
        self.root.addWidget(self.viewer)

        self.root.setCurrentWidget(self.connection)

    def on_mqtt_connect(self):
        """
        Handle the MQTT connection event.
        Switch to the viewer page when the client connects successfully.
        """
        self.root.setCurrentWidget(self.viewer)
