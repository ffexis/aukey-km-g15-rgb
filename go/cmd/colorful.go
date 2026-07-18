package cmd

import (
	"fmt"
	"strings"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/protocol"
)

var colorfulCmd = &cobra.Command{
	Use:   "colorful <on|off>",
	Short: "Enable or disable Colorful mode (multi-color cycling)",
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		state := strings.ToLower(args[0])
		if state != "on" && state != "off" {
			return fmt.Errorf("argument must be 'on' or 'off', got '%s'", args[0])
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

		value := byte(0)
		if state == "on" {
			value = 1
		}

		fmt.Printf("Setting Colorful to %s on profile %d\n", strings.ToUpper(state), profile)

		addr := uint16(protocol.ProfileAddr(protocol.AddrLightColorful, profile))
		packet := protocol.BuildPacket(protocol.CmdRuntime, addr, []byte{value})
		if err := sendCommand(dev, packet); err != nil {
			return err
		}

		fmt.Println("Done!")
		return nil
	},
}

func init() {
	rootCmd.AddCommand(colorfulCmd)
}
