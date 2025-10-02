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
# docs: https://pymodbus.readthedocs.io/en/latest/

from pymodbus.client.serial import ModbusSerialClient
from pymodbus.exceptions import ModbusException
import time

# Configuration
COM_PORT = "COM10"  # Change to your COM port
BAUDRATE = 19200
SLAVE_ID = 2  # Modbus slave address

# Modbus register addresses
COUNTER_ADDRESS = 24575  # Address of the input register to read
BUTTON_INPUT_ADDRESS = 8  # Address of the input to read button state
LED_R_ADDRESS = 8  # Address of the coil to control red LED
LED_G_ADDRESS = 9  # Address of the coil to control green LED
LED_B_ADDRESS = 10  # Address of the coil to control blue LED

# LED color combinations (R, G, B)
LED_STATES = [
    (False, False, False),  # Off
    (True, False, False),  # Red
    (False, True, False),  # Green
    (False, False, True),  # Blue
    (True, True, False),  # Yellow (Red + Green)
    (True, False, True),  # Magenta (Red + Blue)
    (False, True, True),  # Cyan (Green + Blue)
    (True, True, True),  # White (All colors)
]


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


def read_discrete_inputs(client: ModbusSerialClient, address: int, count: int):
    """Read discrete inputs from Modbus slave."""
    try:
        result = client.read_discrete_inputs(address, count=count, device_id=SLAVE_ID)
        if result.isError():
            print(f"Error reading discrete inputs: {result}")
            return None
        return result.bits
    except ModbusException as e:
        print(f"Modbus exception: {e}")
        return None


def write_coil(client: ModbusSerialClient, address: int, value: bool):
    """Write a single coil to Modbus slave."""
    try:
        result = client.write_coil(address, value, device_id=SLAVE_ID)
        if result.isError():
            print(f"Error writing coil: {result}")
            return False
        return True
    except ModbusException as e:
        print(f"Modbus exception: {e}")
        return False


def read_coil(client: ModbusSerialClient, address: int):
    """Read a single coil from Modbus slave."""
    try:
        result = client.read_coils(address, count=1, device_id=SLAVE_ID)
        if result.isError():
            print(f"Error reading coil: {result}")
            return None
        return result.bits[0]
    except ModbusException as e:
        print(f"Modbus exception: {e}")
        return None


def set_rgb_led(client: ModbusSerialClient, RGB: tuple[bool, bool, bool]):
    """Set RGB LED state (tuple of three booleans for R, G, B)."""
    r, g, b = RGB
    success_r = write_coil(client, LED_R_ADDRESS, r)
    success_g = write_coil(client, LED_G_ADDRESS, g)
    success_b = write_coil(client, LED_B_ADDRESS, b)
    return success_r and success_g and success_b


def get_button_state(client: ModbusSerialClient):
    """Get the state of the button (True if pressed)."""
    inputs = read_discrete_inputs(client, BUTTON_INPUT_ADDRESS, count=1)
    if inputs is not None:
        return inputs[0]
    return None


def get_rgb_led_state(client: ModbusSerialClient):
    """Get the current state of the RGB LED (tuple of three booleans for R, G, B)."""
    r = read_coil(client, LED_R_ADDRESS)
    g = read_coil(client, LED_G_ADDRESS)
    b = read_coil(client, LED_B_ADDRESS)
    if r is not None and g is not None and b is not None:
        return (r, g, b)
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
        last_button_state = None
        current_led_state_index = 0
        led_changed = False

        while True:
            loop_time = time.time()

            # Read current values from slave device
            counter_value = get_counter_value(client)
            button_state = get_button_state(client)
            rgb_state = get_rgb_led_state(client)

            # Change LED color every 5 seconds (when seconds are divisible by 5)
            if int(time.time()) % 5 == 0:
                if not led_changed:
                    # Cycle through LED states
                    current_led_state_index = (current_led_state_index + 1) % len(
                        LED_STATES
                    )
                    set_rgb_led(client, LED_STATES[current_led_state_index])
                    led_changed = True
                    rgb_state = get_rgb_led_state(client)
                    print(f"{counter_value} LED state (R,G,B): {rgb_state}")
            else:
                led_changed = False

            # Detect button state changes
            if button_state != last_button_state:
                last_button_state = button_state
                print(f"Button pressed: {button_state}")

            # Maintain consistent loop timing (10ms minimum)
            if time.time() - loop_time < 0.01:
                time.sleep(0.01 - (time.time() - loop_time))

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        # Close connection
        client.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
