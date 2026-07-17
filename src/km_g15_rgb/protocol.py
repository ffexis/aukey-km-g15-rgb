"""Protocol Definitions for AUKEY KM-G15 RGB Control

This protocol was reverse-engineered from USB packet capture analysis.
Commands are sent via HID SET_REPORT (Control Transfer).
"""
from enum import IntEnum
from dataclasses import dataclass
from typing import Tuple, Optional


class Zone(IntEnum):
    """Keyboard zones for RGB control."""
    ZONE_1 = 0x01        # Main keys
    ZONE_2 = 0x02        # Function keys
    ZONE_3 = 0x03        # Navigation keys
    ALL = 0x09           # All zones / global


class LightingMode(IntEnum):
    """Lighting Effect Modes (from Main.ini [Mode] section, 19 modes)."""
    STREAM = 1           # 随波逐流 / Go with the stream
    CLOUDS = 2           # 彩云纷飞 / Clouds fly
    WINDING = 3          # 峰回路转 / Winding paths
    TRIAL = 4            # 光之审判 / The trial of light
    BREATHING = 5        # 呼吸 / Breathing
    STATIC = 6           # 常亮 / Normally on
    SNOW = 7             # 踏雪无痕 / Pass without trace
    RIPPLE = 8           # 泛起涟漪 / Ripple graff
    FAST = 9             # 奔逸绝尘 / Fast run without trace
    STARS = 10           # 繁星点点 / Snow winter jasmine
    FLOWERS = 11         # 百花争艳 / Flowers blooming
    METEOR = 12          # 流星赶月 / Swift action
    HURRICANE = 13       # 大鹏展翅 / Hurricane
    ACCUMULATE = 14      # 厚积薄发 / Accumulate
    DIGITAL = 15         # 落雨纷纷 / Digital Times
    BOTHWAYS = 16        # 左右逢缘 / Both ways
    SURMOUNT = 17        # 众志成城 / Surmount
    FASTFURIOUS = 18     # 速度激情 / Fast and the Furious
    COASTAL = 20         # 指点江山 / Coastal


@dataclass
class RGBColor:
    """RGB Color value."""
    r: int = 0
    g: int = 0
    b: int = 0
    
    def __post_init__(self):
        self.r = max(0, min(255, self.r))
        self.g = max(0, min(255, self.g))
        self.b = max(0, min(255, self.b))
    
    @classmethod
    def from_hex(cls, hex_str: str) -> 'RGBColor':
        """Create color from hex string (e.g., 'ff0000' or '#ff0000')."""
        hex_str = hex_str.lstrip('#')
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex color: {hex_str}")
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return cls(r=r, g=g, b=b)
    
    def to_hex(self) -> str:
        """Convert to hex string."""
        return f"{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to (R, G, B) tuple."""
        return (self.r, self.g, self.b)


class KM_G15_Protocol:
    """Protocol handler for AUKEY KM-G15 RGB keyboard.

    Packet structure (64 bytes):
    - Byte 0: ReportID (0x04)
    - Byte 1: Checksum (sum of bytes 2-63 mod 256)
    - Byte 2: Reserved (0x00)
    - Byte 3: CmdType (command type / memory area)
    - Byte 4: DataLen (length of data following header)
    - Byte 5: Addr_LSB (address low byte)
    - Byte 6: Addr_MSB (address high byte)
    - Byte 7: Reserved (0x00)
    - Byte 8-N: Data Payload
    - Byte N+1-63: Padding (0x00)

    Command flow (three-step sequence):
    1. Start Flag: 04 01 00 01 00 00 00 00 [zeros]
    2. Command packet
    3. End Flag: 04 02 00 02 00 00 00 00 [zeros]
    """
    
    REPORT_ID = 0x04
    PACKET_SIZE = 64
    
    # Command Types
    CMD_READ = 0x03              # Read config
    CMD_SYSTEM_CONFIG = 0x0F     # Global system config
    CMD_KEYMAP = 0x07            # Key mapping / macros
    CMD_RGB_STATIC = 0x11        # Static per-key RGB
    CMD_LED_BUFFER = 0x05        # LED buffer reset
    CMD_RUNTIME_PARAM = 0x06     # Runtime parameters
    
    # Memory Addresses (base for Profile 0)
    # Each profile has its own address space:
    # Profile 0: base + 0x0000
    # Profile 1: base + 0x002A
    # Profile 2: base + 0x0054
    PROFILE_ADDR_OFFSET = 0x002A  # Offset per profile for runtime params

    # Runtime parameter addresses (relative to profile base)
    # These are READ from config (CmdType=0x05) at byte offsets:
    #   Byte 0: Mode
    #   Byte 1: Brightness (0-4, 5 levels)
    #   Byte 2: Colorful (0=off, 1=on)
    #   Byte 3: Direction (0x00=right, 0xFF=left)
    #   Byte 5-7: RGB Color
    
    # WRITE addresses for runtime params (CmdType=0x06):
    ADDR_LIGHT_SPEED = 0x0002       # Animation speed (0-4, 5 levels)
    ADDR_LIGHT_BRIGHTNESS = 0x0001  # Brightness level (0-4, 5 levels)
    ADDR_LIGHT_DIRECTION = 0x0003   # Animation direction (0x00=right, 0xFF=left)
    ADDR_LIGHT_COLORFUL = 0x0004    # Colorful mode toggle (0=off, 1=on)
    ADDR_USB_RATE_BASE = 0x000F     # USB polling rate (0-3)

    # Parameter ranges
    BRIGHTNESS_MIN = 0
    BRIGHTNESS_MAX = 4
    SPEED_MIN = 1
    SPEED_MAX = 5

    # Static RGB addresses (larger offset per profile)
    RGB_ADDR_OFFSET = 0x0200  # Offset per profile for static RGB

    @staticmethod
    def get_profile_addr(base_addr: int, profile: int) -> int:
        """Get the actual address for a given profile."""
        return base_addr + (profile * KM_G15_Protocol.PROFILE_ADDR_OFFSET)
    
    @staticmethod
    def calc_checksum(packet: bytes) -> int:
        """Calculate checksum: sum of bytes[2:] mod 256."""
        if len(packet) < 64:
            packet = packet.ljust(64, b'\x00')
        return sum(packet[2:]) & 0xFF
    
    @staticmethod
    def build_packet(cmd_type: int, addr: int, data: bytes, data_len: int = None) -> bytes:
        """Build a 64-byte packet.

        Args:
            cmd_type: Command type (CmdType)
            addr: Target memory address
            data: Data payload
            data_len: Length override (if None, uses len(data))

        Returns:
            bytes: 64-byte packet
        """
        if data_len is None:
            data_len = len(data)

        # Build header + data
        packet = bytearray(64)
        packet[0] = KM_G15_Protocol.REPORT_ID  # ReportID
        packet[2] = 0x00                         # Reserved
        packet[3] = cmd_type                     # CmdType
        packet[4] = data_len                     # DataLen
        packet[5] = addr & 0xFF                  # Addr_LSB
        packet[6] = (addr >> 8) & 0xFF           # Addr_MSB
        packet[7] = 0x00                         # Reserved

        # Copy data starting at Byte 8
        for i, b in enumerate(data):
            if 8 + i < 64:
                packet[8 + i] = b

        # Calculate and insert checksum
        packet[1] = KM_G15_Protocol.calc_checksum(packet)

        return bytes(packet)
    
    @staticmethod
    def build_start_flag() -> bytes:
        """Build start transaction flag."""
        return KM_G15_Protocol.build_packet(
            cmd_type=0x01,
            addr=0x0000,
            data=bytes([])
        )
    
    @staticmethod
    def build_end_flag() -> bytes:
        """Build end transaction flag."""
        return KM_G15_Protocol.build_packet(
            cmd_type=0x02,
            addr=0x0002,
            data=bytes([])
        )
    
    @staticmethod
    def build_mode_packet(mode: LightingMode, profile: int = 0) -> bytes:
        """Build packet to set lighting mode.

        Args:
            mode: Lighting mode (1-8)
            profile: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        addr = KM_G15_Protocol.get_profile_addr(
            KM_G15_Protocol.ADDR_LIGHT_MODE_BASE, profile
        )
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RUNTIME_PARAM,
            addr=addr,
            data=bytes([mode]),
            data_len=1
        )
    
    @staticmethod
    def build_brightness_packet(brightness: int, profile: int = 0) -> bytes:
        """Build packet to set brightness.

        Args:
            brightness: Brightness value (0-4)
            profile: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        addr = KM_G15_Protocol.get_profile_addr(
            KM_G15_Protocol.ADDR_LIGHT_BRIGHTNESS, profile
        )
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RUNTIME_PARAM,
            addr=addr,
            data=bytes([brightness]),
            data_len=1
        )

    @staticmethod
    def build_speed_packet(speed: int, profile: int = 0) -> bytes:
        """Build packet to set animation speed.

        Args:
            speed: Speed value (1-5)
            profile: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        addr = KM_G15_Protocol.get_profile_addr(
            KM_G15_Protocol.ADDR_LIGHT_SPEED, profile
        )
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RUNTIME_PARAM,
            addr=addr,
            data=bytes([speed]),
            data_len=1
        )

    @staticmethod
    def build_light_on_packet() -> bytes:
        """Build packet to enable RGB lighting (master switch).

        Returns:
            bytes: 64-byte packet
        """
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RUNTIME_PARAM,
            addr=KM_G15_Protocol.ADDR_LIGHT_MODE_BASE,
            data=bytes([0x01]),
            data_len=1
        )

    @staticmethod
    def build_rate_packet(rate_code: int, profile: int = 0) -> bytes:
        """Build packet to set USB polling rate.

        Args:
            rate_code: Rate code (0=125Hz, 1=250Hz, 2=500Hz, 3=1000Hz)
            profile: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        addr = KM_G15_Protocol.get_profile_addr(
            KM_G15_Protocol.ADDR_USB_RATE_BASE, profile
        )
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RUNTIME_PARAM,
            addr=addr,
            data=bytes([rate_code]),
            data_len=1
        )
    
    @staticmethod
    def build_static_color_packet(color: RGBColor, zone: Zone = Zone.ALL) -> bytes:
        """Build packet to set static color.

        Note: This requires more complex data structure for per-key RGB.
        For now, use mode switching.
        """
        # Placeholder - full implementation needs RGB data format
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_RGB_STATIC,
            addr=0x0000,
            data=bytes([]),
            data_len=0
        )

    @staticmethod
    def build_read_packet(addr: int = 0x0000, data_len: int = 44) -> bytes:
        """Build packet to read config from device.

        Args:
            addr: Address to read from
            data_len: Expected data length

        Returns:
            bytes: 64-byte packet
        """
        return KM_G15_Protocol.build_packet(
            cmd_type=KM_G15_Protocol.CMD_READ,
            addr=addr,
            data=bytes(data_len),
            data_len=data_len
        )

    @staticmethod
    def build_profile_switch_packet(profile_index: int) -> bytes:
        """Build packet to switch profile slot.

        Args:
            profile_index: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        if profile_index not in (0, 1, 2):
            raise ValueError("profile_index must be 0, 1, or 2")

        # Magic signature (first 16 bytes)
        magic = bytes([
            0x55, 0xaa, 0xff, 0x02, 0x45, 0x0c, 0x66, 0x76,
            0x03, 0x01, profile_index, 0x18, 0x00, 0x00, 0x00, 0x00
        ])

        # Fixed fill sequence (19 bytes) + 9 zeros
        fill = bytes([
            0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
            0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x11, 0x10, 0x12, 0x14
        ]) + bytes(9)

        data = magic + fill  # Total 44 bytes

        return KM_G15_Protocol.build_packet(
            cmd_type=0x04,
            addr=0x0000,
            data=data,
            data_len=0x2C
        )

    @staticmethod
    def parse_config_response(response: bytes) -> dict:
        """Parse configuration response from device.

        Config data format (from byte 8):
            Byte 0: Mode (1-18, 20)
            Byte 1: Brightness (0-4, 5 levels)
            Byte 2: Colorful (0=OFF, 1=ON)
            Byte 3: Direction (0x00=Right, 0xFF=Left)
            Byte 5-7: RGB Color (R, G, B)

        Args:
            response: 64-byte response from device

        Returns:
            dict: Parsed configuration
        """
        if len(response) < 16:
            return {"error": "Response too short"}

        # Config data starts at byte 8
        config = response[8:]

        return {
            "mode": config[0] if len(config) > 0 else 0,
            "brightness": config[1] if len(config) > 1 else 0,
            "colorful": bool(config[2]) if len(config) > 2 else False,
            "direction": "left" if config[3] == 0xff else "right" if len(config) > 3 else "unknown",
            "color": RGBColor(
                r=config[5] if len(config) > 5 else 0,
                g=config[6] if len(config) > 6 else 0,
                b=config[7] if len(config) > 7 else 0
            ),
        }

    @staticmethod
    def build_read_config_packet(profile: int = 0) -> bytes:
        """Build packet to read full configuration for a profile.

        Args:
            profile: Profile slot (0, 1, or 2)

        Returns:
            bytes: 64-byte packet
        """
        addr = profile * 0x0200  # Each profile has 0x200 offset for config
        return KM_G15_Protocol.build_packet(
            cmd_type=0x05,
            addr=addr,
            data=bytes(56),
            data_len=56
        )

    @staticmethod
    def build_read_runtime_packet(profile: int, offset: int) -> bytes:
        """Build packet to read runtime parameter.

        Args:
            profile: Profile slot (0, 1, or 2)
            offset: Runtime parameter offset (0x000F for USB Rate, 0x002B for Speed)

        Returns:
            bytes: 64-byte packet
        """
        addr = profile * 0x0200 + offset
        return KM_G15_Protocol.build_packet(
            cmd_type=0x05,
            addr=addr,
            data=bytes(16),
            data_len=16
        )
