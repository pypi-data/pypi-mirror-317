from __future__ import annotations
import sys
import os

from PySide6.QtWidgets import QApplication

from .MqttHandler import get_mqtt_handler
from .App import App

from .utils import get_user_data_dir


def main():
    data_dir = get_user_data_dir()
    os.makedirs(data_dir, exist_ok=True)

    app = QApplication()

    mqtt = get_mqtt_handler()
    mqtt.max_messages = 100

    gui = App()
    gui.show()

    sys.exit(app.exec())
