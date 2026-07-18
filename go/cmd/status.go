package cmd

import (
	"fmt"
	"time"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/effects"
	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var statusCmd = &cobra.Command{
	Use:   "status",
	Short: "Read current device configuration",
	RunE: func(cmd *cobra.Command, args []string) error {
		dev, err := openDevice()
		if err != nil {
			return err
		}
		defer dev.Close()

		profileIndex, err := resolveProfile(dev)
		if err != nil {
			return err
		}

		fmt.Printf("Device Status:\n")
		fmt.Printf("  Current Profile: %d\n\n", profileIndex)

		// Read full configuration (speed is included in config response)
		readCmd := protocol.BuildReadConfigPacket(profileIndex)
		if err := dev.SendReport(readCmd[:]); err != nil {
			return fmt.Errorf("send read config: %w", err)
		}

		time.Sleep(500 * time.Millisecond)
		response, err := dev.Read(1000)
		if err != nil {
			return fmt.Errorf("read config: %w", err)
		}
		if response == nil || len(response) < 16 {
			return fmt.Errorf("failed to read configuration")
		}

		config := protocol.ParseConfigResponse(response)

		// Speed is stored in config flash at byte 2 (hw value 0-4)
		// Convert to user-facing value (1=slowest, 5=fastest)
		speed := protocol.HWToUserSpeed(config.Speed)

		rateHz := protocol.RateCodeToHz(config.USBRate)

		cn, en, _ := effects.GetModeName(config.Mode)

		fmt.Printf("Profile %d Configuration:\n", profileIndex)
		fmt.Printf("  Mode: %d (%s / %s)\n", config.Mode, cn, en)
		fmt.Printf("  Brightness: %d\n", config.Brightness)
		fmt.Printf("  Speed: %d\n", speed)
		fmt.Printf("  Direction: %s\n", config.Direction)
		if config.Colorful {
			fmt.Printf("  Colorful: ON\n")
		} else {
			fmt.Printf("  Colorful: OFF\n")
		}
		fmt.Printf("  Color: #%02x%02x%02x\n", config.Color.R, config.Color.G, config.Color.B)
		fmt.Printf("  USB Rate: %dHz (code=%d)\n", rateHz, config.USBRate)

		return nil
	},
}

func init() {
	rootCmd.AddCommand(statusCmd)
}
