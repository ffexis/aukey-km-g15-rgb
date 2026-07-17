"""Test setting only one value at a time"""
import sys
sys.path.insert(0, r'F:\Dev Project\km-g15-kb-reverse-eng\src')
from km_g15_rgb.device import KM_G15_Device
from km_g15_rgb.protocol import KM_G15_Protocol
import time


def set_value(device, addr, value):
    """Set a single value"""
    start = KM_G15_Protocol.build_start_flag()
    device.send_report(start)
    
    cmd = KM_G15_Protocol.build_packet(
        cmd_type=0x06,
        addr=addr,
        data=bytes([value]),
        data_len=1
    )
    device.send_report(cmd)
    
    end = KM_G15_Protocol.build_end_flag()
    device.send_report(end)
    time.sleep(0.3)


def read_config(device):
    """Read and return config"""
    read_cmd = KM_G15_Protocol.build_read_config_packet(0)
    device.send_report(read_cmd)
    time.sleep(0.3)
    response = device.read(timeout_ms=500)
    if response and len(response) >= 16:
        return response[8:]
    return None


def print_config(config, label=""):
    """Print config bytes"""
    if config:
        print("%s:" % label)
        print("  Byte 0 (Mode): %d" % config[0])
        print("  Byte 1: %d" % config[1])
        print("  Byte 2: %d" % config[2])
        print("  Byte 3: %d" % config[3])
        print("  Byte 4: %d" % config[4])
        print("  Byte 5-7: %02x %02x %02x" % (config[5], config[6], config[7]))
    print()


print("=== Test: Sequential set and read ===\n")

with KM_G15_Device() as device:
    # First, read current config
    print("--- Initial state ---")
    config = read_config(device)
    print_config(config, "Current")
    
    # Set brightness (addr 0x0001) to 3
    print("--- Setting Addr 0x0001 = 3 ---")
    set_value(device, 0x0001, 3)
    config = read_config(device)
    print_config(config, "After set")
    
    # Set speed (addr 0x0002) to 4
    print("--- Setting Addr 0x0002 = 4 ---")
    set_value(device, 0x0002, 4)
    config = read_config(device)
    print_config(config, "After set")
    
    # Set direction (addr 0x0003) to 0xff
    print("--- Setting Addr 0x0003 = 0xff ---")
    set_value(device, 0x0003, 0xff)
    config = read_config(device)
    print_config(config, "After set")
    
    # Set mode (addr 0x0000) to 6
    print("--- Setting Addr 0x0000 = 6 ---")
    set_value(device, 0x0000, 6)
    config = read_config(device)
    print_config(config, "After set")
