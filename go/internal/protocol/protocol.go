// Package protocol implements the AUKEY KM-G15 USB HID protocol.
//
// Packet structure (64 bytes):
//   - Byte 0:  ReportID (0x04)
//   - Byte 1:  Checksum (sum of bytes[2..63] mod 256)
//   - Byte 2:  Reserved (0x00)
//   - Byte 3:  CmdType
//   - Byte 4:  DataLen
//   - Byte 5:  Addr_LSB
//   - Byte 6:  Addr_MSB
//   - Byte 7:  Reserved (0x00)
//   - Byte 8+: Data payload
//   - Rest:    Zero padding
package protocol

import "fmt"

const (
	ReportID   byte = 0x04
	PacketSize      = 64

	// Command types
	CmdStart    byte = 0x01
	CmdEnd      byte = 0x02
	CmdRead     byte = 0x03
	CmdProfile  byte = 0x04
	CmdLEDBuf   byte = 0x05
	CmdConfigRead byte = 0x05 // Used for reading config/runtime params (same value as LED_BUF)
	CmdRuntime  byte = 0x06
	CmdKeyMap   byte = 0x07
	CmdSysCfg   byte = 0x0F
	CmdRGBStatic byte = 0x11

	// Runtime parameter addresses (relative to profile base, CmdType=0x06)
	AddrLightMode       = 0x0000
	AddrLightBrightness = 0x0001
	AddrLightSpeed      = 0x0002
	AddrLightDirection  = 0x0003
	AddrLightColorful   = 0x0004
	AddrUSBRateBase     = 0x000F

	// Profile address offsets
	ProfileAddrOffset = 0x002A // 42 bytes per profile
	RGBAddrOffset     = 0x0200 // Offset per profile for static RGB

	// Parameter ranges
	BrightnessMin = 0
	BrightnessMax = 4
	SpeedMin      = 0
	SpeedMax      = 4

	// LED buffer addresses (CmdType=0x05)
	LEDBufAddr0 = 0x0000
	LEDBufAddr1 = 0x002A
	LEDBufAddr2 = 0x0054
)

// RGBColor represents an RGB color value.
type RGBColor struct {
	R, G, B byte
}

// DeviceConfig holds parsed device configuration.
type DeviceConfig struct {
	Mode       int
	Brightness int
	Speed      int // Hardware value (0-4); user value = 4 - Speed
	Direction  string
	Colorful   bool
	Color      RGBColor
	USBRate    int
}

// ProfileAddr returns the actual address for a given profile.
func ProfileAddr(baseAddr int, profile int) int {
	return baseAddr + profile*ProfileAddrOffset
}

// CalcChecksum computes the checksum: sum of bytes[2..63] mod 256.
func CalcChecksum(packet []byte) byte {
	var sum int
	for i := 2; i < len(packet) && i < PacketSize; i++ {
		sum += int(packet[i])
	}
	return byte(sum & 0xFF)
}

// BuildPacket constructs a 64-byte packet.
func BuildPacket(cmdType byte, addr uint16, data []byte) [PacketSize]byte {
	var packet [PacketSize]byte
	packet[0] = ReportID
	packet[2] = 0x00
	packet[3] = cmdType
	packet[4] = byte(len(data))
	packet[5] = byte(addr & 0xFF)
	packet[6] = byte((addr >> 8) & 0xFF)
	packet[7] = 0x00

	n := len(data)
	if n > PacketSize-8 {
		n = PacketSize - 8
	}
	copy(packet[8:], data[:n])

	packet[1] = CalcChecksum(packet[:])
	return packet
}

// BuildStartFlag builds the start transaction flag packet.
func BuildStartFlag() [PacketSize]byte {
	return BuildPacket(CmdStart, 0x0000, nil)
}

// BuildEndFlag builds the end transaction flag packet.
func BuildEndFlag() [PacketSize]byte {
	return BuildPacket(CmdEnd, 0x0002, nil)
}

// BuildModePacket builds a packet to set lighting mode.
func BuildModePacket(mode int, profile int) [PacketSize]byte {
	addr := uint16(ProfileAddr(AddrLightMode, profile))
	return BuildPacket(CmdRuntime, addr, []byte{byte(mode)})
}

// BuildBrightnessPacket builds a packet to set brightness.
func BuildBrightnessPacket(brightness int, profile int) [PacketSize]byte {
	addr := uint16(ProfileAddr(AddrLightBrightness, profile))
	return BuildPacket(CmdRuntime, addr, []byte{byte(brightness)})
}

// BuildSpeedPacket builds a packet to set animation speed.
// The speed value should be the hardware value (0-4), not the user-facing value.
func BuildSpeedPacket(hwSpeed int, profile int) [PacketSize]byte {
	addr := uint16(ProfileAddr(AddrLightSpeed, profile))
	return BuildPacket(CmdRuntime, addr, []byte{byte(hwSpeed)})
}

// BuildRatePacket builds a packet to set USB polling rate.
// rateCode: 0=125Hz, 1=250Hz, 2=500Hz, 3=1000Hz.
func BuildRatePacket(rateCode int, profile int) [PacketSize]byte {
	addr := uint16(ProfileAddr(AddrUSBRateBase, profile))
	return BuildPacket(CmdRuntime, addr, []byte{byte(rateCode)})
}

// BuildLightOnPacket builds a packet to enable RGB lighting (master switch).
func BuildLightOnPacket() [PacketSize]byte {
	return BuildPacket(CmdRuntime, AddrLightMode, []byte{0x01})
}

// BuildReadPacket builds a packet to read config from device.
func BuildReadPacket(addr uint16, dataLen int) [PacketSize]byte {
	return BuildPacket(CmdRead, addr, make([]byte, dataLen))
}

// BuildProfileSwitchPacket builds a packet to switch profile slot.
func BuildProfileSwitchPacket(profileIndex int) ([PacketSize]byte, error) {
	if profileIndex < 0 || profileIndex > 2 {
		return [PacketSize]byte{}, fmt.Errorf("profile_index must be 0, 1, or 2, got %d", profileIndex)
	}

	// Magic signature (first 16 bytes)
	magic := []byte{
		0x55, 0xaa, 0xff, 0x02, 0x45, 0x0c, 0x66, 0x76,
		0x03, 0x01, byte(profileIndex), 0x18, 0x00, 0x00, 0x00, 0x00,
	}

	// Fixed fill sequence (19 bytes) + 9 zeros
	fill := []byte{
		0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09,
		0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x11, 0x10, 0x12, 0x14,
	}
	fill = append(fill, make([]byte, 9)...)

	data := append(magic, fill...) // Total 44 bytes
	return BuildPacket(CmdProfile, 0x0000, data), nil
}

// BuildReadConfigPacket builds a packet to read full configuration for a profile.
func BuildReadConfigPacket(profile int) [PacketSize]byte {
	addr := uint16(profile * 0x002A)
	return BuildPacket(CmdConfigRead, addr, make([]byte, 56))
}

// BuildReadRuntimePacket builds a packet to read a runtime parameter.
func BuildReadRuntimePacket(offset int) [PacketSize]byte {
	return BuildPacket(CmdConfigRead, uint16(offset), make([]byte, 16))
}

// ParseConfigResponse parses a 64-byte configuration response from the device.
func ParseConfigResponse(response []byte) DeviceConfig {
	cfg := DeviceConfig{
		Direction: "unknown",
	}

	if len(response) < 16 {
		return cfg
	}

	payload := response[8:]
	if len(payload) > 42 {
		payload = payload[:42]
	}

	if len(payload) > 0 {
		cfg.Mode = int(payload[0])
	}
	if len(payload) > 1 {
		cfg.Brightness = int(payload[1])
	}
	if len(payload) > 2 {
		cfg.Speed = int(payload[2])
	}
	if len(payload) > 3 {
		if payload[3] == 0xFF {
			cfg.Direction = "left"
		} else {
			cfg.Direction = "right"
		}
	}
	if len(payload) > 4 {
		cfg.Colorful = payload[4] != 0
	}
	if len(payload) > 5 {
		cfg.Color.R = payload[5]
	}
	if len(payload) > 6 {
		cfg.Color.G = payload[6]
	}
	if len(payload) > 7 {
		cfg.Color.B = payload[7]
	}
	if len(payload) > 15 {
		cfg.USBRate = int(payload[15])
	}

	return cfg
}

// RateCodeToHz converts a rate code to Hz value.
func RateCodeToHz(code int) int {
	switch code {
	case 0:
		return 125
	case 1:
		return 250
	case 2:
		return 500
	case 3:
		return 1000
	default:
		return code
	}
}

// HzToRateCode converts Hz value to rate code.
func HzToRateCode(hz int) (int, error) {
	switch hz {
	case 125:
		return 0, nil
	case 250:
		return 1, nil
	case 500:
		return 2, nil
	case 1000:
		return 3, nil
	default:
		return 0, fmt.Errorf("invalid rate: %d Hz (valid: 125, 250, 500, 1000)", hz)
	}
}

// UserSpeedToHW converts user-facing speed (0-4) to hardware value (0-4).
func UserSpeedToHW(userSpeed int) int {
	return 4 - userSpeed
}

// HWToUserSpeed converts hardware speed (0-4) to user-facing value (0-4).
func HWToUserSpeed(hwSpeed int) int {
	return 4 - hwSpeed
}
