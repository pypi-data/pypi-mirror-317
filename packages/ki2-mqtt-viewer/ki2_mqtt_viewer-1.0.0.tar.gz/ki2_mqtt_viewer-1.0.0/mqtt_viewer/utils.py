from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import TypedDict, NotRequired, Literal
from pathlib import Path
import json

from platformdirs import user_data_dir

if TYPE_CHECKING:
    pass


def get_user_data_dir():
    """
    Get the user data directory specific to the application.

    :return: Path to the user data directory.
    """
    app_name = "MQTT-viewer"
    app_author = "ki2"
    return user_data_dir(app_name, app_author)


class AuthData(TypedDict):
    """
    Represents authentication data including username and password.
    """

    username: str
    password: str


class ProfileJson(TypedDict):
    """
    Represents the structure of a profile JSON object.

    Attributes:
        version: The version of the profile format.
        host: The MQTT host address.
        port: The MQTT port.
        auth: Optional authentication data.
        topics: Optional list of topics.
    """

    version: Literal[1]
    host: str
    port: int
    auth: NotRequired[AuthData | None]
    topics: NotRequired[list[str]]


def load_profile(path: Path | str) -> ProfileJson:
    """
    Load a profile JSON from a file.

    :param path: Path to the JSON file.
    :return: A ProfileJson object.
    """
    with open(path, "r") as f:
        return json.load(f)


def save_profile(path: Path | str, profile: ProfileJson):
    """
    Save a profile JSON to a file.

    :param path: Path to the file where the profile will be saved.
    :param profile: The ProfileJson object to save.
    """
    with open(path, "w") as f:
        json.dump(profile, f, indent=2)


def generate_profile(
    host: str, port: int, username: str | None = None, password: str | None = None
) -> ProfileJson:
    """
    Generate a profile JSON object based on provided parameters.

    :param host: The MQTT host address.
    :param port: The MQTT port.
    :param username: Optional username for authentication.
    :param password: Optional password for authentication.
    :return: A ProfileJson object.
    :raises ValueError: If only one of username or password is provided.
    """

    profile: ProfileJson = {
        "version": 1,
        "host": host,
        "port": port,
    }
    if isinstance(username, str):
        username = username.strip()
    if isinstance(password, str):
        password = password.strip()

    if username == "":
        username = None
    if password == "":
        password = None

    if username is not None and password is not None:
        profile["auth"] = {
            "username": username,
            "password": password,
        }

    if username is not None and password is None:
        raise ValueError("Password is required if username is provided")
    if username is None and password is not None:
        raise ValueError("Username is required if password is provided")
    return profile
