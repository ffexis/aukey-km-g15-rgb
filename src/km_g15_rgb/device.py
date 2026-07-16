"""USB HID Device Communication Layer"""
import hid
from typing import Optional, List


class KM_G15_Device:
    """AUKEY KM-G15 USB HID device wrapper."""
    
    # Known VID/PID for AUKEY KM-G15 (SONiX chip)
    VENDOR_ID = 0x0C45
    PRODUCT_ID = 0x7666
    
    # Usage Pages
    USAGE_PAGE_KEYBOARD = 0x01
    USAGE_PAGE_VENDOR = 0xFF1C
    
    # Usages
    USAGE_KEYBOARD = 0x06
    USAGE_VENDOR_RGB = 0x0092
    
    # Report ID for RGB control
    REPORT_ID = 0x04
    
    def __init__(self):
        self._device: Optional[hid.device] = None
        self._vendor_device_info: Optional[dict] = None
    
    @staticmethod
    def enumerate_devices() -> List[dict]:
        """Enumerate all KM-G15 devices."""
        devices = hid.enumerate(KM_G15_Device.VENDOR_ID, KM_G15_Device.PRODUCT_ID)
        return devices
    
    @staticmethod
    def find_rgb_interface() -> Optional[dict]:
        """Find the vendor-specific RGB control interface."""
        devices = hid.enumerate(KM_G15_Device.VENDOR_ID, KM_G15_Device.PRODUCT_ID)
        for d in devices:
            if d.get('usage_page') == KM_G15_Device.USAGE_PAGE_VENDOR:
                return d
        return None
    
    def open(self, serial_number: Optional[str] = None) -> bool:
        """Open the RGB control interface."""
        rgb_interface = self.find_rgb_interface()
        if not rgb_interface:
            raise RuntimeError("RGB control interface not found. Is the keyboard connected?")

        self._vendor_device_info = rgb_interface
        self._device = hid.device()

        try:
            # Use open_path() to precisely open the RGB interface
            self._device.open_path(rgb_interface['path'])
            return True
        except Exception as e:
            self._device = None
            raise RuntimeError(f"Failed to open device: {e}")
    
    def close(self):
        """Close the device connection."""
        if self._device:
            try:
                self._device.close()
            except:
                pass
            self._device = None
    
    def write(self, data: bytes) -> int:
        """Write data to the device (Output Report)."""
        if not self._device:
            raise RuntimeError("Device not open")

        # Send raw 64-byte packet
        data_list = list(data)
        return self._device.write(data_list)
    
    def send_report(self, packet: bytes) -> bool:
        """Send a 64-byte RGB control packet."""
        if len(packet) != 64:
            raise ValueError(f"Packet must be 64 bytes, got {len(packet)}")

        result = self.write(packet)
        return result == 64

    def read(self, timeout_ms: int = 100) -> Optional[bytes]:
        """Read data from the device."""
        if not self._device:
            raise RuntimeError("Device not open")

        try:
            data = self._device.read(64, timeout_ms)
            if data:
                return bytes(data)
            return None
        except Exception:
            return None
    
    def get_manufacturer_string(self) -> Optional[str]:
        """Get the manufacturer string."""
        if not self._device:
            return None
        try:
            return self._device.get_manufacturer_string()
        except:
            return None
    
    def get_product_string(self) -> Optional[str]:
        """Get the product string."""
        if not self._device:
            return None
        try:
            return self._device.get_product_string()
        except:
            return None
    
    def __enter__(self):
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
