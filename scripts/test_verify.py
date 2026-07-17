"""Set user described state and verify"""
import sys
sys.path.insert(0, r'F:\Dev Project\km-g15-kb-reverse-eng\src')
from km_g15_rgb.device import KM_G15_Device
from km_g15_rgb.protocol import KM_G15_Protocol
import time


def send_cmd(device, cmd_type, addr, data):
    """Send a command with start/end flags"""
    start = KM_G15_Protocol.build_start_flag()
    device.send_report(start)
    
    cmd = KM_G15_Protocol.build_packet(
        cmd_type=cmd_type,
        addr=addr,
        data=bytes(data),
        data_len=len(data)
    )
    device.send_report(cmd)
    
    end = KM_G15_Protocol.build_end_flag()
    device.send_report(end)
    time.sleep(0.2)


def read_config(device, profile=0):
    """Read config for a profile"""
    read_cmd = KM_G15_Protocol.build_read_config_packet(profile)
    device.send_report(read_cmd)
    time.sleep(0.3)
    response = device.read(timeout_ms=500)
    if response and len(response) >= 16:
        return response[8:]
    return None


def print_config(config, label=""):
    """Print config"""
    if config:
        print("%s:" % label)
        print("  Mode: %d" % config[0])
        print("  Speed: %d" % config[1])
        print("  Colorful: %d (%s)" % (config[2], "ON" if config[2] else "OFF"))
        print("  Direction: %d (%s)" % (config[3], "Left" if config[3] == 0xff else "Right"))
        print("  Color: #%02x%02x%02x" % (config[5], config[6], config[7]))
    print()


print("=== Set user described state and verify ===\n")

with KM_G15_Device() as device:
    # Read initial state
    print("--- Initial state ---")
    config = read_config(device, 0)
    print_config(config, "Current")
    
    # Set mode to 2
    print("--- Setting mode=2 ---")
    send_cmd(device, 0x06, 0x0000, [2])
    config = read_config(device, 0)
    print_config(config, "After")
    
    # Set speed to 4
    print("--- Setting speed=4 ---")
    send_cmd(device, 0x06, 0x0002, [4])
    config = read_config(device, 0)
    print_config(config, "After")
    
    # Set direction to right (0x00)
    print("--- Setting direction=0 (right) ---")
    send_cmd(device, 0x06, 0x0003, [0x00])
    config = read_config(device, 0)
    print_config(config, "After")
    
    # Set colorful to ON (1)
    print("--- Setting colorful=1 (ON) ---")
    send_cmd(device, 0x06, 0x0004, [1])
    config = read_config(device, 0)
    print_config(config, "After")
    
    print("=== Expected ===")
    print("  Mode: 2")
    print("  Speed: 4")
    print("  Colorful: 1 (ON)")
    print("  Direction: 0 (Right)")
