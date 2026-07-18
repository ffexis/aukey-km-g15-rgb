package cmd

import (
	"fmt"
	"strconv"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var rateCmd = &cobra.Command{
	Use:   "rate <hz>",
	Short: "Set USB polling rate (125, 250, 500, 1000)",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		hz, err := strconv.Atoi(args[0])
		if err != nil {
			return fmt.Errorf("invalid rate: %s (valid: 125, 250, 500, 1000)", args[0])
		}

		rateCode, err := protocol.HzToRateCode(hz)
		if err != nil {
			return err
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

		fmt.Printf("Setting USB rate to %dHz on profile %d\n", hz, profile)

		packet := protocol.BuildRatePacket(rateCode, profile)
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(rateCmd)
}
