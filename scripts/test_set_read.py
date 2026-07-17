"""Test set and read back to verify field mapping"""
import sys
sys.path.insert(0, r'F:\Dev Project\km-g15-kb-reverse-eng\src')
from km_g15_rgb.device import KM_G15_Device
from km_g15_rgb.protocol import KM_G15_Protocol
import time


def set_and_read(device, addr, value, name):
    """Set a value and read back config to verify"""
    # Set value
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
    
    # Read config
    read_cmd = KM_G15_Protocol.build_read_config_packet(0)
    device.send_report(read_cmd)
    time.sleep(0.3)
    response = device.read(timeout_ms=500)
    
    if response:
        config = response[8:]
        print("Set %s=%d -> Read back:" % (name, value))
        print("  Byte 0 (Mode): %d" % config[0])
        print("  Byte 1 (Speed?): %d" % config[1])
        print("  Byte 2 (Colorful?): %d" % config[2])
        print("  Byte 3 (Direction?): %d" % config[3])
        print("  Byte 4: %d" % config[4])
        print("  Byte 5-7: %02x %02x %02x" % (config[5], config[6], config[7]))
        print()


print("=== Test: Set values and read back ===\n")

with KM_G15_Device() as device:
    # Test setting brightness (addr 0x0001)
    print("--- Testing Addr 0x0001 ---")
    set_and_read(device, 0x0001, 3, "Addr 0x0001")
    
    # Test setting speed (addr 0x0002)
    print("--- Testing Addr 0x0002 ---")
    set_and_read(device, 0x0002, 2, "Addr 0x0002")
    
    # Test setting direction (addr 0x0003)
    print("--- Testing Addr 0x0003 ---")
    set_and_read(device, 0x0003, 0xff, "Addr 0x0003")
    
    # Test setting colorful (addr 0x0004)
    print("--- Testing Addr 0x0004 ---")
    set_and_read(device, 0x0004, 0, "Addr 0x0004")
