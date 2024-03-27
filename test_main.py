import socket
import time


def send_ur_script_cmd(ip, port, script):
    """
    Send URScript commands directly to the UR robot via socket connection.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            print(f"Successfully connected to {ip}:{port}")
            s.sendall(script.encode('utf8'))
            time.sleep(1)  # Wait for the command to execute
    except OSError as e:
        print(f"Failed to connect to {ip}:{port}. Error: {e}")

def control_rg2_gripper(ip, target_width=110, target_force=40, payload=0.5, set_payload=False, depth_compensation=False, slave=False, wait=2):
    """
    Control the RG2 gripper on a UR robot.
    """
    # Correct the command to set digital output
    set_payload_cmd = "True" if set_payload else "False"
    depth_compensation_cmd = "True" if depth_compensation else "False"
    slave_cmd = "True" if slave else "False"

    # Script to control the gripper
    script = f"""
    def rg2_control():
        textmsg("Activating RG2 Gripper")
        set_tool_voltage(24)
        rg_data = floor({target_width} + 9.2) * 4 + floor({target_force} / 2) * 4 * 111 + 32768
        rg_data = rg_data + 16384 if {slave_cmd} else rg_data
        write_output_integer_register(0, rg_data)
        sleep(0.1)
        set_digital_out(8, True)
        sleep(0.1)
        set_digital_out(8, False)
        sleep({wait})
        popup("RG2 Gripper activated", title="Gripper Status", warning=False)
    end
    rg2_control()
    """
    send_ur_script_cmd(ip, 30002, script)

if __name__ == "__main__":
    ip_address = "192.168.125.101"  # Change to the IP address of your UR robot
    # Adjust the parameters as needed for your specific use case
    control_rg2_gripper(ip_address, target_width=60, target_force=40, wait=2)
