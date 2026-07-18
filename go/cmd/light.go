package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var lightCmd = &cobra.Command{
	Use:   "light",
	Short: "Enable RGB lighting (master switch)",
	RunE: func(cmd *cobra.Command, args []string) error {
		dev, err := openDevice()
		if err != nil {
			return err
		}
		defer dev.Close()

		fmt.Println("Enabling RGB lighting...")

		packet := protocol.BuildLightOnPacket()
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(lightCmd)
}
