package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/effects"
	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var modeCmd = &cobra.Command{
	Use:   "mode <mode-id>",
	Short: "Set lighting effect mode",
	Long: `Set lighting effect mode by ID.

Available modes: 1-18, 20 (use 'list-modes' to see all)
If --profile is not specified, the command targets the currently active profile.`,
	Args: cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		var modeID int
		if _, err := fmt.Sscanf(args[0], "%d", &modeID); err != nil {
			return fmt.Errorf("invalid mode ID: %s", args[0])
		}

		if !effects.IsValidMode(modeID) {
			return fmt.Errorf("invalid mode %d", modeID)
		}

		cn, en, _ := effects.GetModeName(modeID)

		dev, err := openDevice()
		if err != nil {
			return err
		}
		defer dev.Close()

		profile, err := resolveProfile(dev)
		if err != nil {
			return err
		}

		fmt.Printf("Setting mode to %d: %s (%s) on profile %d\n", modeID, cn, en, profile)

		packet := protocol.BuildModePacket(modeID, profile)
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(modeCmd)
}
