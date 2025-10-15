# -------------------------------
# Simple MQTT Demo
# -------------------------------
# This script demonstrates basic MQTT concepts using paho-mqtt:
# - Connecting to an MQTT broker
# - Publishing messages to topics
# - Subscribing to topics and receiving messages

import paho.mqtt.client as mqtt  # MQTT client library
import time  # For delays between operations

# MQTT Broker settings
BROKER_HOST = "broker.hivemq.com"  # Public test broker (free MQTT broker for testing)
BROKER_PORT = 1883  # Standard MQTT port (unencrypted)

# Topic configuration - MQTT uses hierarchical topics separated by forward slashes
BASE_TOPIC = "r_d/industrial-automation"  # Root topic namespace
SENSOR_ID = "ondrejs-home"  # Unique identifier for this sensor/device
TOPIC = f"{BASE_TOPIC}/demo/{SENSOR_ID}/sensor/temperature"  # Full topic path


def on_connect(client, userdata, flags, rc):
    """
    Callback function triggered when client connects to MQTT broker.

    Args:
        client: The MQTT client instance
        userdata: User-defined data (not used here)
        flags: Response flags from broker
        rc: Connection result code (0 = success)
    """
    if rc == 0:
        print("Connected to MQTT broker")
        # Subscribe to our topic after successful connection
        # This means we'll receive any messages published to this topic
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    """
    Callback function triggered when a message is received on a subscribed topic.

    Args:
        client: The MQTT client instance
        userdata: User-defined data (not used here)
        msg: Message object containing topic, payload, QoS, etc.
    """
    topic = msg.topic  # Which topic the message was received on
    payload = msg.payload.decode("utf-8")  # Message content (decoded from bytes)
    print(f"Received: {payload} on topic: {topic}")


def main():
    """Main function that demonstrates MQTT publish/subscribe functionality."""
    print("=== Simple MQTT Demo ===")
    print("This demo will publish and receive messages on the same topic\n")

    # Create MQTT client instance
    # This represents our connection to the MQTT broker
    client = mqtt.Client()

    # Register callback functions
    # These functions will be called automatically when events occur
    client.on_connect = on_connect  # Called when connection is established
    client.on_message = on_message  # Called when message is received

    # Connect to the MQTT broker
    print(f"Connecting to {BROKER_HOST}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)  # 60 = keepalive timeout in seconds

    # Start the network loop in background thread
    # This handles network traffic, callbacks, and reconnections
    client.loop_start()

    # Wait for connection to be established
    time.sleep(2)

    try:
        # Publish temperature readings (simulate sensor data)
        for i in range(5):
            payload = 20 + i  # Simulate temperature values: 20, 21, 22, 23, 24

            # Publish message to the topic
            # Any subscriber to this topic will receive this message
            client.publish(TOPIC, payload)
            print(f"Published: {payload}")

            # Wait 3 seconds before next reading
            time.sleep(3)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Ctrl+C -> Demo stopped")

    finally:
        # Clean up: stop network loop and disconnect
        client.loop_stop()  # Stop the background network thread
        client.disconnect()  # Close connection to broker
        print("Disconnected")


# Run the demo if this script is executed directly
if __name__ == "__main__":
    main()
