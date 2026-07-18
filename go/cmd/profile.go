package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var profileCmd = &cobra.Command{
	Use:   "profile <0|1|2>",
	Short: "Switch active profile slot (0-2)",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		var profileIndex int
		if _, err := fmt.Sscanf(args[0], "%d", &profileIndex); err != nil {
			return fmt.Errorf("invalid profile: %s", args[0])
		}

		if profileIndex < 0 || profileIndex > 2 {
			return fmt.Errorf("profile must be 0, 1, or 2, got %d", profileIndex)
		}

		dev, err := openDevice()
		if err != nil {
			return err
		}
		defer dev.Close()

		fmt.Printf("Switching to profile %d\n", profileIndex)

		packet, err := protocol.BuildProfileSwitchPacket(profileIndex)
		if err != nil {
			return err
		}
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(profileCmd)
}
