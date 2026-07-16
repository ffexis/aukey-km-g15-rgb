"""Analyze KM-G15 RGB protocol from capture data"""
import re
from pathlib import Path

def parse_capture_file(file_path):
    """Parse the raw capture data and extract RGB commands"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all lines with potential RGB data
    lines = content.split('\n')
    
    rgb_commands = []
    init_commands = []
    
    for line in lines:
        # Look for lines with hex data
        match = re.search(r'[\da-f]{4}\s+([\da-f\s]+)', line)
        if match:
            hex_data = match.group(1).strip()
            parts = hex_data.split()
            
            if len(parts) >= 16:
                # Check for RGB command pattern: 2a 00 00 [zone] [mode] 02 01 00 00 [r] [g] [b] 08
                if parts[0] == '2a' and parts[1] == '00' and parts[2] == '00':
                    zone = int(parts[3], 16)
                    mode = int(parts[4], 16)
                    r = int(parts[8], 16)
                    g = int(parts[9], 16)
                    b = int(parts[10], 16)
                    brightness = int(parts[11], 16)
                    
                    rgb_commands.append({
                        'zone': zone,
                        'mode': mode,
                        'r': r,
                        'g': g,
                        'b': b,
                        'brightness': brightness,
                        'raw': hex_data
                    })
                
                # Check for init command: 55 aa ff
                elif parts[3] == '55' and parts[4] == 'aa' and parts[5] == 'ff':
                    init_commands.append(hex_data)
    
    return rgb_commands, init_commands

def analyze_commands(rgb_commands):
    """Analyze RGB commands to understand the protocol"""
    
    print("=" * 60)
    print("AUKEY KM-G15 RGB Protocol Analysis")
    print("=" * 60)
    
    # Group commands by zone
    zones = {}
    for cmd in rgb_commands:
        zone = cmd['zone']
        if zone not in zones:
            zones[zone] = []
        zones[zone].append(cmd)
    
    print(f"\nTotal RGB commands found: {len(rgb_commands)}")
    print(f"Unique zones: {sorted(zones.keys())}")
    
    print("\n" + "-" * 60)
    print("Zone Analysis:")
    print("-" * 60)
    
    for zone in sorted(zones.keys()):
        commands = zones[zone]
        print(f"\nZone 0x{zone:02x}:")
        
        # Find unique colors
        colors = set()
        for cmd in commands:
            colors.add((cmd['r'], cmd['g'], cmd['b']))
        
        print(f"  Unique colors: {len(colors)}")
        for r, g, b in sorted(colors):
            print(f"    RGB: ({r:3d}, {g:3d}, {b:3d}) = #{r:02x}{g:02x}{b:02x}")
    
    # Detect protocol structure
    print("\n" + "-" * 60)
    print("Protocol Structure:")
    print("-" * 60)
    
    if rgb_commands:
        sample = rgb_commands[0]
        print(f"""
Packet format (inferred):
  Byte 0-2: 2a 00 00    (Command header)
  Byte 3:   {sample['zone']:02x}        (Zone ID)
  Byte 4:   {sample['mode']:02x}        (Mode/type)
  Byte 5-7: 01 00 00    (Parameters)
  Byte 8-10: {sample['r']:02x} {sample['g']:02x} {sample['b']:02x}     (RGB color)
  Byte 11:  {sample['brightness']:02x}        (Brightness?)
  Byte 12-15: 00 00 00 00 (Padding)

Zone IDs:
  0x01 = Zone 1 (possibly main keys)
  0x02 = Zone 2 (possibly function keys)
  0x03 = Zone 3 (possibly navigation keys)
  0x09 = Zone 9 (possibly all zones / global)

Mode values:
  0x00 = Off/Static?
  0x02 = Static color?
""")
    
    return zones

def main():
    capture_file = Path(r"F:\Dev Project\km-g15-kb-reverse-eng\captures\raw_data.txt")
    
    if not capture_file.exists():
        print(f"Error: {capture_file} not found")
        return
    
    print(f"Analyzing: {capture_file}")
    print()
    
    rgb_commands, init_commands = parse_capture_file(capture_file)
    
    if init_commands:
        print("Init commands found:")
        for cmd in init_commands[:3]:
            print(f"  {cmd}")
        print()
    
    if rgb_commands:
        zones = analyze_commands(rgb_commands)
        
        # Save analysis results
        output_file = capture_file.parent / "protocol_analysis.txt"
        with open(output_file, 'w') as f:
            f.write("AUKEY KM-G15 RGB Protocol Analysis\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total RGB commands: {len(rgb_commands)}\n")
            f.write(f"Unique zones: {sorted(zones.keys())}\n\n")
            
            for zone in sorted(zones.keys()):
                commands = zones[zone]
                f.write(f"Zone 0x{zone:02x}: {len(commands)} commands\n")
        
        print(f"\nAnalysis saved to: {output_file}")
    else:
        print("No RGB commands found in capture data")

if __name__ == "__main__":
    main()
