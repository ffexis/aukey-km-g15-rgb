package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/device"
	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

// Version is set at build time via -ldflags
var Version = "dev"

var (
	globalProfile *int
	globalDevice  *string
)

var rootCmd = &cobra.Command{
	Use:     "km-g15-rgb",
	Version: Version,
	Short:   "AUKEY KM-G15 RGB Keyboard Control",
	Long:    "A CLI tool for controlling RGB lighting on the AUKEY KM-G15 mechanical keyboard via USB HID.",
}

func init() {
	globalProfile = rootCmd.PersistentFlags().IntP("profile", "p", -1, "Target profile slot (0-2, default: auto-detect)")
	globalDevice = rootCmd.PersistentFlags().String("device", "", "Specific device path (if multiple keyboards)")
}

// Execute runs the root command.
func Execute() {
	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

// openDevice opens the device, using --device path if provided, otherwise auto-detecting.
func openDevice() (*device.Device, error) {
	if *globalDevice != "" {
		return device.Open(*globalDevice)
	}
	return device.OpenDefault()
}

// resolveProfile returns the target profile, auto-detecting if not specified.
func resolveProfile(dev *device.Device) (int, error) {
	if *globalProfile >= 0 {
		if *globalProfile > 2 {
			return 0, fmt.Errorf("profile must be 0, 1, or 2, got %d", *globalProfile)
		}
		return *globalProfile, nil
	}
	return readCurrentProfile(dev)
}

// readCurrentProfile reads the active profile from the device.
func readCurrentProfile(dev *device.Device) (int, error) {
	cmd := protocol.BuildReadPacket(0x0000, 44)
	if err := dev.SendReport(cmd[:]); err != nil {
		return 0, fmt.Errorf("send read command: %w", err)
	}

	response, err := dev.Read(500)
	if err != nil {
		return 0, fmt.Errorf("read response: %w", err)
	}
	if response == nil || len(response) < 19 {
		return 0, fmt.Errorf("no response from device")
	}

	return int(response[18]), nil
}

// sendCommand executes a three-step command sequence (start → cmd → end).
func sendCommand(dev *device.Device, cmdPacket [protocol.PacketSize]byte) error {
	start := protocol.BuildStartFlag()
	if err := dev.SendReport(start[:]); err != nil {
		return fmt.Errorf("send start: %w", err)
	}

	if err := dev.SendReport(cmdPacket[:]); err != nil {
		return fmt.Errorf("send command: %w", err)
	}

	end := protocol.BuildEndFlag()
	if err := dev.SendReport(end[:]); err != nil {
		return fmt.Errorf("send end: %w", err)
	}

	return nil
}
