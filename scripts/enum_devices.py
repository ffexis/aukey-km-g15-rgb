"""Enumerate all HID devices to find AUKEY KM-G15"""
import hid

devices = hid.enumerate()
print(f"Found {len(devices)} HID devices:\n")
print(f"{'VID':>6} {'PID':>6} | {'Product':<40} | {'Manufacturer':<30} | Usage Page:Usage")
print("-" * 120)

for d in devices:
    vid = d['vendor_id']
    pid = d['product_id']
    product = d.get('product_string', 'N/A')
    manufacturer = d.get('manufacturer_string', 'N/A')
    usage_page = d.get('usage_page', 0)
    usage = d.get('usage', 0)
    interface = d.get('interface_number', -1)
    
    print(f"0x{vid:04x} 0x{pid:04x} | {product:<40} | {manufacturer:<30} | 0x{usage_page:04x}:0x{usage:04x} (if={interface})")

print("\n" + "=" * 120)
print("Filtering for likely AUKEY devices (looking for keyboard-related entries):")
print("=" * 120)

# Filter for keyboard-related devices
keyboard_devices = [d for d in devices if d.get('usage_page') == 0x01 and d.get('usage') == 0x06]  # Generic Desktop / Keyboard
print(f"\nKeyboard devices (Usage 01:06): {len(keyboard_devices)}")
for d in keyboard_devices:
    print(f"  VID: 0x{d['vendor_id']:04x} PID: 0x{d['product_id']:04x} | {d.get('product_string', 'N/A')} | {d.get('manufacturer_string', 'N/A')}")

# Also check for consumer control devices (volume, media keys)
consumer_devices = [d for d in devices if d.get('usage_page') == 0x01 and d.get('usage') == 0x05]  # Generic Desktop / Consumer Control
print(f"\nConsumer Control devices (Usage 01:05): {len(consumer_devices)}")
for d in consumer_devices:
    print(f"  VID: 0x{d['vendor_id']:04x} PID: 0x{d['product_id']:04x} | {d.get('product_string', 'N/A')} | {d.get('manufacturer_string', 'N/A')}")

# Check for vendor-specific devices (might be RGB control interface)
vendor_devices = [d for d in devices if d.get('usage_page', 0) >= 0xFF00]
print(f"\nVendor-specific devices (Usage Page >= 0xFF00): {len(vendor_devices)}")
for d in vendor_devices:
    print(f"  VID: 0x{d['vendor_id']:04x} PID: 0x{d['product_id']:04x} | {d.get('product_string', 'N/A')} | {d.get('manufacturer_string', 'N/A')} | Usage: 0x{d.get('usage_page', 0):04x}:0x{d.get('usage', 0):04x}")
