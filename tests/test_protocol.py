"""Tests for km-g15-rgb protocol module"""
import pytest
from km_g15_rgb.protocol import RGBColor, Zone, LightingMode, KM_G15_Protocol


class TestRGBColor:
    def test_from_hex(self):
        color = RGBColor.from_hex("ff0000")
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_from_hex_with_hash(self):
        color = RGBColor.from_hex("#00ff00")
        assert color.r == 0
        assert color.g == 255
        assert color.b == 0
    
    def test_to_hex(self):
        color = RGBColor(255, 128, 0)
        assert color.to_hex() == "ff8000"
    
    def test_to_tuple(self):
        color = RGBColor(10, 20, 30)
        assert color.to_tuple() == (10, 20, 30)
    
    def test_clamping(self):
        color = RGBColor(300, -10, 128)
        assert color.r == 255
        assert color.g == 0
        assert color.b == 128
    
    def test_invalid_hex(self):
        with pytest.raises(ValueError):
            RGBColor.from_hex("xyz")
        with pytest.raises(ValueError):
            RGBColor.from_hex("ff00")


class TestProtocol:
    def test_build_static_color(self):
        color = RGBColor(255, 0, 0)
        packet = KM_G15_Protocol.build_static_color(color)
        
        # Check header
        assert packet[0:3] == bytes([0x2a, 0x00, 0x00])
        # Check zone (all)
        assert packet[3] == Zone.ALL
        # Check RGB (bytes 9-11)
        assert packet[9] == 255  # R
        assert packet[10] == 0   # G
        assert packet[11] == 0   # B
    
    def test_build_static_color_zone1(self):
        color = RGBColor(0, 255, 0)
        packet = KM_G15_Protocol.build_static_color(color, Zone.ZONE_1)
        
        assert packet[3] == Zone.ZONE_1
        assert packet[10] == 255  # G
    
    def test_build_off_packet(self):
        packet = KM_G15_Protocol.build_off_packet()
        
        # Check header
        assert packet[0:3] == bytes([0x2a, 0x00, 0x00])
        # Check RGB is all zeros (bytes 9-11)
        assert packet[9] == 0
        assert packet[10] == 0
        assert packet[11] == 0
    
    def test_packet_size(self):
        packet = KM_G15_Protocol.build_static_color(RGBColor(255, 255, 255))
        assert len(packet) == 17  # 17 bytes per captured protocol


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
