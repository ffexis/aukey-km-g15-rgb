package cmd

import (
	"fmt"
	"time"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var speedCmd = &cobra.Command{
	Use:   "speed <value>",
	Short: "Set animation speed (0=slowest, 4=fastest)",
	Long: `Set animation speed. The value is user-facing (0-4).
Hardware stores speed inverted (0=fastest, 4=slowest), the conversion is automatic.`,
	Args: cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		var userSpeed int
		if _, err := fmt.Sscanf(args[0], "%d", &userSpeed); err != nil {
			return fmt.Errorf("invalid speed value: %s", args[0])
		}

		if userSpeed < protocol.SpeedMin || userSpeed > protocol.SpeedMax {
			return fmt.Errorf("speed must be %d-%d, got %d",
				protocol.SpeedMin, protocol.SpeedMax, userSpeed)
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

		hwSpeed := protocol.UserSpeedToHW(userSpeed)
		fmt.Printf("Setting speed to %d on profile %d\n", userSpeed, profile)

		packet := protocol.BuildSpeedPacket(hwSpeed, profile)
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		// Wait for device to commit changes to flash
		time.Sleep(500 * time.Millisecond)

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(speedCmd)
}
