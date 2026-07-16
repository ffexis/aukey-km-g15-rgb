"""Analyze new USB capture data"""
import json
import re
from pathlib import Path

def extract_data_fragments(file_path):
    """Extract data fragments from JSON capture file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fragments = []
    for packet in data:
        layers = packet.get('_source', {}).get('layers', {})
        setup_data = layers.get('Setup Data', {})
        
        if 'usb.data_fragment' in setup_data:
            fragment = setup_data['usb.data_fragment']
            # Parse hex string
            hex_bytes = bytes.fromhex(fragment.replace(':', ' '))
            fragments.append(hex_bytes)
    
    return fragments

def analyze_fragment(data):
    """Analyze a single data fragment"""
    if len(data) < 10:
        return None
    
    report_id = data[0]
    # Parse based on pattern
    result = {
        'report_id': report_id,
        'raw': data[:20].hex(),
        'hex_display': ' '.join(f'{b:02x}' for b in data[:20])
    }
    
    return result

def main():
    captures_dir = Path(r"F:\Dev Project\km-g15-kb-reverse-eng\captures\new")
    
    print("=" * 70)
    print("AUKEY KM-G15 USB Protocol Analysis")
    print("=" * 70)
    
    # Analyze software start
    print("\n[1] Software Start Data")
    print("-" * 70)
    fragments = extract_data_fragments(captures_dir / "software start.json")
    print(f"Found {len(fragments)} packets")
    
    for i, frag in enumerate(fragments):
        print(f"\nPacket {i+1}: {frag[:20].hex()}")
    
    # Analyze light effects
    print("\n\n[2] Light Effects 1-8 Data")
    print("-" * 70)
    fragments = extract_data_fragments(captures_dir / "light effect 1 to 8.json")
    print(f"Found {len(fragments)} packets")
    
    # Group by pattern
    patterns = {}
    for frag in fragments:
        # Extract key bytes (skip first byte which is report ID)
        key = frag[1:6].hex() if len(frag) >= 6 else frag.hex()
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(frag)
    
    print(f"\nUnique patterns: {len(patterns)}")
    
    for pattern, frags in sorted(patterns.items()):
        print(f"\nPattern: {pattern}")
        print(f"  Count: {len(frags)}")
        if frags:
            print(f"  Example: {frags[0][:20].hex()}")
    
    # Analyze USB report rate
    print("\n\n[3] USB Report Rate Data")
    print("-" * 70)
    fragments = extract_data_fragments(captures_dir / "usb report rate 125-250-500-1000.json")
    print(f"Found {len(fragments)} packets")
    
    for i, frag in enumerate(fragments):
        print(f"\nPacket {i+1}: {frag[:20].hex()}")

if __name__ == "__main__":
    main()
