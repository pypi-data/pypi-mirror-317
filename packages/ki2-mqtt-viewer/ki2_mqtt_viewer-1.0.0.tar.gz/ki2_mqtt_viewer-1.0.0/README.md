# MQTT Viewer

MQTT Viewer is a user-friendly application designed to help users interact with MQTT brokers effortlessly. With an intuitive interface, it allows users to connect to an MQTT server, view and log messages for different topics, and publish messages with ease.

## Features

- **Connect to MQTT Brokers**:

  - Enter the server address, port, and optional authentication details.
  - Save and load connection profiles for future use.

- **Manage Topics**:

  - Topics are automatically added as messages are received.
  - View a list of available topics.
  - Add custom topics manually.

- **Message Logging**:

  - View incoming and outgoing messages for selected topics.
  - Messages are color-coded for clarity.

- **Send Messages**:

  - Compose and send messages to any topic.

## Installation

### Step 1: Install the Application

1. Open a terminal on your system.
2. Run the following command to install MQTT Viewer using `pip`:
   ```bash
   pip install ki2-mqtt-viewer
   ```

### Step 2: Run the Application

1. After installation, launch the application by typing:
   ```bash
   mqtt-viewer
   ```
2. The graphical interface will open, allowing you to connect to your MQTT broker.

## Usage

1. **Launch the Application**:
   Run the command `mqtt-viewer` in your terminal to start the application.

2. **Connect to an MQTT Broker**:

   - Enter the server address (default: `localhost`) and port (default: `1883`).
   - If the broker requires authentication, check the box and provide your username and password.
   - Click **Connect** to establish a connection.

3. **Save a Connection Profile**:

   - After entering your connection details, click **Save Profile** to store them for future use.
   - Use **Load Profile** to quickly reconnect.

4. **View Topics and Messages**:

   - Once connected, topics will be automatically added as messages are received.
   - Browse the list of topics and click a topic to view its message log.

5. **Send a Message**:

   - Select a topic from the list or add one manually if necessary.
   - Enter your message in the input field and click **Send**.

## License

This application is licensed under the MIT License. See the LICENSE file for more details.
