# -------------------------------
# Modbus RTU Master Demo
# -------------------------------
# This demo connects to a Modbus slave device and demonstrates:
# - Reading counter values from input registers
# - Reading button state from discrete inputs
# - Controlling RGB LED via coils
# - Automatic LED color cycling every 5 seconds
#
# Install pymodbus if needed:
# pip install pymodbus

from pymodbus.client.serial import ModbusSerialClient
from pymodbus.exceptions import ModbusException
import time

# Configuration
COM_PORT = "COM10"  # Change to your COM port
BAUDRATE = 19200
SLAVE_ID = 2  # Modbus slave address

# Modbus register addresses
COUNTER_ADDRESS = 24575  # Address of the input register to read


def read_input_registers(client: ModbusSerialClient, address: int, count: int):
    """Read input registers from Modbus slave."""
    try:
        result = client.read_input_registers(address, count=count, device_id=SLAVE_ID)
        if result.isError():
            print(f"Error reading registers: {result}")
            return None
        return result.registers
    except ModbusException as e:
        print(f"Modbus exception: {e}")
        return None


def get_counter_value(client: ModbusSerialClient):
    """Get the current value of the counter from input registers."""
    regs = read_input_registers(client, COUNTER_ADDRESS, count=2)
    if regs is not None and len(regs) == 2:
        # Combine two 16-bit registers into one 32-bit integer (little-endian)
        return (regs[1] << 16) | regs[0]
    return None


def main():
    print(f"Connecting to Modbus slave on {COM_PORT}...")
    # Create Modbus RTU client with serial communication parameters
    client = ModbusSerialClient(
        port=COM_PORT, baudrate=BAUDRATE, timeout=1, parity="N", stopbits=1, bytesize=8
    )
    # Connect to the slave
    if not client.connect():
        print("Failed to connect to Modbus slave")
        return

    print("Connected successfully!")

    try:
        # Continuous monitoring loop
        print("\n--- Continuous monitoring ---")
        while True:
            # Read current values from slave device
            counter_value = get_counter_value(client)
            print(f"\rCounter: {counter_value}")
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        # Close connection
        client.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
