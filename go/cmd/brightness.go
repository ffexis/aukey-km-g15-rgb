package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var brightnessCmd = &cobra.Command{
	Use:   "brightness <value>",
	Short: "Set brightness level (0=min, 4=max)",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		var brightness int
		if _, err := fmt.Sscanf(args[0], "%d", &brightness); err != nil {
			return fmt.Errorf("invalid brightness value: %s", args[0])
		}

		if brightness < protocol.BrightnessMin || brightness > protocol.BrightnessMax {
			return fmt.Errorf("brightness must be %d-%d, got %d",
				protocol.BrightnessMin, protocol.BrightnessMax, brightness)
		}

		dev, err := openDevice()
		if err != nil {
			return err
		}
		defer dev.Close()

		profile, err := resolveProfile(dev)
		if err != nil {
			return err
		}

		fmt.Printf("Setting brightness to %d on profile %d\n", brightness, profile)

		packet := protocol.BuildBrightnessPacket(brightness, profile)
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(brightnessCmd)
}
