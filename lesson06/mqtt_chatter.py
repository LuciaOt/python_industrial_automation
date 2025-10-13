# -------------------------------
# Simple MQTT Chatter
# -------------------------------
# This script creates a simple MQTT client that can publish and subscribe
# to a chat topic, allowing users to send and receive messages in real-time.

import json
import paho.mqtt.client as mqttc
import logging

# Configure logging to display info level messages
logging.basicConfig(level=logging.INFO)

# MQTT Broker configuration
HOST = "broker.hivemq.com"  # Public HiveMQ broker
PORT = 1883  # Standard MQTT port
BASE_TOPIC = "r_d/industrial-automation"
CHATROOM_NAME = "lesson"
USERNAME = "ondra"  # Change this to your username

# Topic structure for chat messages and status updates
CHAT_TOPIC = f"{BASE_TOPIC}/chatroom/{CHATROOM_NAME}/msg"
STATUS_TOPIC = f"{BASE_TOPIC}/chatroom/status"


def on_message(client, userdata, msg):
    """
    Callback function for handling chat messages.
    Parses JSON payload and displays user messages.
    """
    # payload is utf-8 encoded string so we need to decode it first
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        user = payload.get("user")
        message = payload.get("message")
        if user and message:
            logging.info(f"{user}: {message}")
        else:
            logging.warning(f"UnknownUser: {msg.payload.decode('utf-8')}")
    except Exception as e:
        logging.error(e)


def on_user_status(client, userdata, msg):
    """
    Callback function for handling user status messages.
    Shows when users connect/disconnect.
    """
    logging.info(f"STATUS: {msg.payload.decode('utf-8')}")


def on_subscribe(client, userdata, mid, granted_qos, properties):
    """Callback when successfully subscribed to topics."""
    logging.info("Subscribed")


def on_disconnect(client, userdata, rc, properties):
    """Callback when client disconnects from broker."""
    logging.info(f"Disconnected {rc}")


def on_connect(client: mqttc.Client, userdata, flags, rc, properties):
    """
    Callback when client connects to broker.
    Subscribes to chat and status topics, announces user connection.
    """
    # Subscribe to both chat messages and status updates with different QoS levels
    client.subscribe([(CHAT_TOPIC, 1), (STATUS_TOPIC, 2)])

    # Announce that this user has connected
    client.publish(STATUS_TOPIC, payload=f"{USERNAME} connected")
    logging.info(f"Connected {rc}")


def main():
    """
    Main function that sets up MQTT client and handles user input.
    Creates a chat interface where users can type messages.
    """
    # Create MQTT client using MQTTv5 protocol
    client = mqttc.Client(protocol=mqttc.MQTTv5)
    client.enable_logger(logging.getLogger())

    # Set up callback functions for different events
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    # Set up specific message callbacks for different topics
    client.message_callback_add(STATUS_TOPIC, on_user_status)
    client.message_callback_add(CHAT_TOPIC, on_message)

    # Set a "last will" message that will be sent if client disconnects unexpectedly
    client.will_set(STATUS_TOPIC, payload=f"{USERNAME} disconnected")

    # Connect to the MQTT broker and start the network loop
    client.connect(HOST, PORT)
    client.loop_start()  # Start background thread for network operations
    logging.info("Loop started")

    try:
        # Main chat loop - read user input and publish messages
        while True:
            message = input()  # Wait for user to type a message

            # Create JSON payload with username and message
            payload = {"user": USERNAME, "message": message}
            json_payload = json.dumps(payload)

            # Publish message to chat topic with QoS 2 (exactly once delivery)
            client.publish(CHAT_TOPIC, payload=json_payload, qos=2, retain=False)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    finally:
        # Clean shutdown - announce disconnection and close connection
        client.publish(
            STATUS_TOPIC, payload=f"{USERNAME} disconnected"
        ).wait_for_publish(
            5
        )  # Wait up to 5 seconds for message to be sent
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Closing")
