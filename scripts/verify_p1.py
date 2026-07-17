"""Verify Profile 1 config"""
import sys
sys.path.insert(0, r'F:\Dev Project\km-g15-kb-reverse-eng\src')
from km_g15_rgb.device import KM_G15_Device
from km_g15_rgb.protocol import KM_G15_Protocol
from km_g15_rgb.effects import get_mode_name
import time

print('=== Verify Profile 1 config ===')
print('User described: p1, accumulate(14), brightness=4, speed=2, color 00FFFF, colorful=false, direction=right')
print()

with KM_G15_Device() as device:
    read_cmd = KM_G15_Protocol.build_read_config_packet(1)
    device.send_report(read_cmd)
    time.sleep(0.3)
    response = device.read(timeout_ms=500)
    
    if response:
        raw = response[8:15]
        
        print('Raw config bytes (Byte 8-14):')
        print('  %s' % ' '.join('%02x' % b for b in raw))
        
        print()
        print('Parsed fields:')
        print('  Byte 0 (Mode): %d' % raw[0])
        print('  Byte 1 (Brightness): %d' % raw[1])
        print('  Byte 2 (Colorful): %d' % raw[2])
        print('  Byte 3 (Direction): %d (%s)' % (raw[3], 'Left' if raw[3] == 0xff else 'Right'))
        print('  Byte 4 (Reserved): %d' % raw[4])
        print('  Byte 5: %d (0x%02x)' % (raw[5], raw[5]))
        print('  Byte 6: %d (0x%02x)' % (raw[6], raw[6]))
        
        print()
        print('Color analysis:')
        print('  If G-R-B: R=0x%02x G=0x%02x' % (raw[6], raw[5]))
        print('  If R-G-B: R=0x%02x G=0x%02x' % (raw[5], raw[6]))
        
        cn, en = get_mode_name(raw[0])
        print()
        print('Mode match: %s (expected: accumulate/14)' % ('YES' if raw[0] == 14 else 'NO'))
        print('Brightness match: %s (expected: 4)' % ('YES' if raw[1] == 4 else 'NO'))
