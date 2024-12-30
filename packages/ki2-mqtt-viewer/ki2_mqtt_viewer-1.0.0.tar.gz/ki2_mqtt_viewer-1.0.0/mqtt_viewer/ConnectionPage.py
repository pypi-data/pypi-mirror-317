from __future__ import annotations
from typing import TYPE_CHECKING
from pathlib import Path
import traceback

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QFormLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtCore import Qt

from .MqttHandler import get_mqtt_handler
from .SignalManager import get_signal_manager

from .utils import generate_profile, save_profile, load_profile, get_user_data_dir

if TYPE_CHECKING:
    pass


class ConnectionPage(QWidget):

    root_layout: QVBoxLayout
    form_layout: QFormLayout

    address_field: QLineEdit
    port_field: QLineEdit
    auth_checkbox: QCheckBox
    username_label: QLabel
    username_field: QLineEdit
    password_label: QLabel
    password_field: QLineEdit
    connect_button: QPushButton

    save_profile_button: QPushButton
    load_profile_button: QPushButton

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Initializes the ConnectionPage widget and builds the UI layout.
        """
        super().__init__(parent)
        self.build()

    def build(self):
        """
        Configure the user interface by setting up layout, fields, and buttons.
        """
        self.root_layout = QVBoxLayout()
        self.root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.root_layout)

        # Form container to hold the labels and fields in a compact view
        form_container = QWidget()
        self.form_layout = QFormLayout()
        form_container.setLayout(self.form_layout)
        self.root_layout.addWidget(
            form_container, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Address and port
        self.address_field = QLineEdit("localhost")
        self.form_layout.addRow("Address:", self.address_field)

        self.port_field = QLineEdit("1883")
        self.form_layout.addRow("Port:", self.port_field)

        # Check box for auth
        self.auth_checkbox = QCheckBox("Authentication?")
        self.auth_checkbox.stateChanged.connect(self.toggle_auth_fields)
        self.root_layout.addWidget(
            self.auth_checkbox, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Username and password fields
        self.username_label = QLabel("Username:")
        self.username_field = QLineEdit()
        self.form_layout.addRow(self.username_label, self.username_field)

        self.password_label = QLabel("Password:")
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.form_layout.addRow(self.password_label, self.password_field)

        # Hide username and password fields by default
        self.username_label.hide()
        self.password_label.hide()
        self.username_field.hide()
        self.password_field.hide()

        # Connection button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_server)
        self.root_layout.addWidget(
            self.connect_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Spacer to add space between the Connect button and the Save/Load profile
        # buttons
        self.root_layout.addSpacerItem(
            QSpacerItem(
                0,
                40,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Fixed,
            )
        )

        # Save and Load profile buttons
        buttons_layout = QHBoxLayout()
        self.save_profile_button = QPushButton("Save Profile")
        self.load_profile_button = QPushButton("Load Profile")
        buttons_layout.addWidget(self.save_profile_button)
        buttons_layout.addWidget(self.load_profile_button)
        self.root_layout.addLayout(buttons_layout)
        self.save_profile_button.clicked.connect(self.save_profile)
        self.load_profile_button.clicked.connect(self.load_profile)

    def toggle_auth_fields(self, state: Qt.CheckState) -> None:
        """
        Show or hide authentication fields based on the checkbox state.

        :param state: The state of the checkbox (checked or unchecked).
        """
        if state == Qt.CheckState.Checked.value:
            self.username_label.show()
            self.username_field.show()
            self.password_label.show()
            self.password_field.show()
        else:
            self.username_label.hide()
            self.username_field.hide()
            self.password_label.hide()
            self.password_field.hide()

    def connect_to_server(self) -> None:
        """
        Connect to the MQTT server using the provided settings. Handles authentication
        if specified. Displays an error message if the connection fails.
        """
        address: str = self.address_field.text()
        port: int = int(self.port_field.text())
        use_auth: bool = self.auth_checkbox.isChecked()
        username: str | None = None
        password: str | None = None

        if use_auth:
            username = self.username_field.text()
            password = self.password_field.text()

        try:
            mqtt = get_mqtt_handler()
            mqtt.connect_settings(address, port, username, password)
            mqtt.connect()
            get_signal_manager().emit_connected()
        except Exception as e:
            print(traceback.format_exc())
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setInformativeText(str(e))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()

    def save_profile(self) -> None:
        """
        Opens a file dialog to save the connection profile as a JSON file. Checks if
        the file already exists and asks for confirmation to overwrite.
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Profile", get_user_data_dir(), "JSON Files (*.json)"
        )
        if not file_path:
            return

        if not file_path.lower().endswith(".json"):
            file_path += ".json"

        try:
            if file_path.endswith("settings.json"):
                raise ValueError(
                    "Reserved file name 'settings.json'."
                    "Please choose a different name."
                )

            if Path(file_path).exists():
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("Confirm Overwrite")
                msg_box.setText(f'The file "{file_path}" already exists.')
                msg_box.setInformativeText("Do you want to overwrite it?")
                msg_box.setStandardButtons(
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                msg_box.setDefaultButton(QMessageBox.StandardButton.No)

                result = msg_box.exec()

                if result != QMessageBox.StandardButton.Yes:
                    return

            port = int(self.port_field.text())
            use_auth = self.auth_checkbox.isChecked()
            username = self.username_field.text() if use_auth else None
            password = self.password_field.text() if use_auth else None
            profile = generate_profile(
                self.address_field.text(), port, username, password
            )
            save_profile(file_path, profile)

        except ValueError as e:
            print(traceback.format_exc())
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setInformativeText(str(e))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return

    def load_profile(self) -> None:
        """
        Opens a file dialog to load a connection profile from a JSON file. Updates
        the fields based on the loaded profile.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Profile", get_user_data_dir(), "JSON Files (*.json)"
        )
        if not file_path:
            return

        try:
            if not file_path.lower().endswith(".json"):
                raise Exception(f"Invalid file type: {file_path} (JSON expected)")

            profile = load_profile(file_path)
            if profile is None:
                return

            self.address_field.setText(profile.get("host", "localhost"))
            self.port_field.setText(str(profile.get("port", "1883")))
            auth = profile.get("auth", None)
            self.auth_checkbox.setChecked(auth is not None)
            if auth is not None:
                self.username_field.setText(auth.get("username", ""))
                self.password_field.setText(auth.get("password", ""))

            topics = profile.get("topics", [])
            if len(topics) > 0:
                for topic in topics:
                    get_signal_manager().emit_new_topic(topic)

        except Exception as e:
            print(traceback.format_exc())
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setInformativeText(str(e))
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            return
