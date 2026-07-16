"""USB Capture Helper Script using tshark
Usage: Run this script, then quickly operate the AUKEY software RGB settings.
The script will capture for 30 seconds then stop.
"""
import subprocess
import time
import os

TSHARK_CMD = r"C:\Program Files\Wireshark\tshark.exe"
CAPTURE_DIR = r"F:\Dev Project\km-g15-kb-reverse-eng\captures"
CAPTURE_FILE = os.path.join(CAPTURE_DIR, "capture.pcap")
CAPTURE_DURATION = 30  # seconds
INTERFACE = "USBPcap3"  # Keyboard is on USBPcap3

def main():
    print("=" * 60)
    print("AUKEY KM-G15 USB Capture Helper (tshark)")
    print("=" * 60)
    print()
    print(f"Capture file: {CAPTURE_FILE}")
    print(f"Interface: {INTERFACE}")
    print(f"Duration: {CAPTURE_DURATION} seconds")
    print()
    print("INSTRUCTIONS:")
    print("1. Keep this window open")
    print("2. Open AUKEY software NOW (have it ready)")
    print("3. Press Enter here to START capture")
    print("4. IMMEDIATELY do these in AUKEY software (30 seconds):")
    print("   - Switch to Static mode -> set Red -> Green -> Blue")
    print("   - Switch to Breathing mode")
    print("   - Switch to Wave mode")
    print("   - Adjust brightness low -> high")
    print("   - Adjust speed slow -> fast")
    print()
    
    input("Press Enter to START capture...")
    
    print()
    print("[*] Starting USB capture...")
    
    # Start tshark
    cmd = [
        TSHARK_CMD,
        "-i", INTERFACE,
        "-w", CAPTURE_FILE,
        "-a", f"duration:{CAPTURE_DURATION}"  # Auto-stop after duration
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"[*] Capture started (PID: {process.pid})")
    print(f"[*] OPERATE AUKEY SOFTWARE NOW!")
    print(f"[*] Capture will run for {CAPTURE_DURATION} seconds...")
    print()
    
    # Wait for capture duration
    for i in range(CAPTURE_DURATION):
        remaining = CAPTURE_DURATION - i
        print(f"\r[*] Time remaining: {remaining:2d}s ", end="", flush=True)
        time.sleep(1)
    
    print()
    print()
    print("[*] Stopping capture...")
    
    # Stop the process
    process.terminate()
    try:
        process.wait(timeout=5)
    except:
        process.kill()
    
    # Check if file was created
    if os.path.exists(CAPTURE_FILE):
        size = os.path.getsize(CAPTURE_FILE)
        print(f"[+] Capture saved: {CAPTURE_FILE}")
        print(f"[+] File size: {size:,} bytes")
        
        if size > 0:
            print()
            print("=" * 60)
            print("NEXT STEPS:")
            print("1. The capture file is ready for analysis!")
            print("2. Tell me to analyze it")
            print("=" * 60)
        else:
            print("[-] WARNING: File is empty!")
    else:
        print("[-] ERROR: Capture file not created!")
    
    print()


if __name__ == "__main__":
    main()
