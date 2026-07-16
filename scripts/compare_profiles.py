"""Compare profile 0 and profile 1 light-on commands"""
import json
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
            hex_bytes = bytes.fromhex(fragment.replace(':', ' '))
            fragments.append(hex_bytes)
    
    return fragments

def analyze_fragment(data):
    """Analyze a single data fragment"""
    if len(data) < 10:
        return None
    
    return {
        'report_id': data[0],
        'checksum': data[1],
        'cmd_type': data[3],
        'data_len': data[4],
        'addr_lsb': data[5],
        'addr_msb': data[6],
        'raw': ' '.join(f'{b:02x}' for b in data[:20])
    }

def main():
    captures_dir = Path(r"F:\Dev Project\km-g15-kb-reverse-eng\captures\new")
    
    print("=" * 70)
    print("Comparing Profile 0 vs Profile 1 Light-On Commands")
    print("=" * 70)
    
    # Profile 0
    print("\n[Profile 0] Light-on + switch effect")
    print("-" * 70)
    fragments_0 = extract_data_fragments(captures_dir / "profile 0 light-on switch light effect.json")
    print(f"Total packets: {len(fragments_0)}")
    
    for i, frag in enumerate(fragments_0):
        info = analyze_fragment(frag)
        if info:
            print(f"\nPacket {i+1}:")
            print(f"  Cmd: 0x{info['cmd_type']:02x}, Addr: 0x{info['addr_msb']:02x}{info['addr_lsb']:02x}, DataLen: {info['data_len']}")
            print(f"  Raw: {info['raw']}")
    
    # Profile 1
    print("\n\n[Profile 1] Light-on + switch effect")
    print("-" * 70)
    fragments_1 = extract_data_fragments(captures_dir / "profile 1 light-on switch light effect.json")
    print(f"Total packets: {len(fragments_1)}")
    
    for i, frag in enumerate(fragments_1):
        info = analyze_fragment(frag)
        if info:
            print(f"\nPacket {i+1}:")
            print(f"  Cmd: 0x{info['cmd_type']:02x}, Addr: 0x{info['addr_msb']:02x}{info['addr_lsb']:02x}, DataLen: {info['data_len']}")
            print(f"  Raw: {info['raw']}")
    
    # Compare first few packets
    print("\n\n" + "=" * 70)
    print("COMPARISON: First 10 packets")
    print("=" * 70)
    
    min_len = min(len(fragments_0), len(fragments_1), 10)
    for i in range(min_len):
        frag0 = fragments_0[i]
        frag1 = fragments_1[i]
        
        same = frag0 == frag1
        marker = "SAME" if same else "DIFF"
        
        print(f"\nPacket {i+1} [{marker}]:")
        print(f"  P0: {frag0[:16].hex()}")
        print(f"  P1: {frag1[:16].hex()}")

if __name__ == "__main__":
    main()
