package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/device"
)

var infoCmd = &cobra.Command{
	Use:   "info",
	Short: "Show connected device information",
	RunE: func(cmd *cobra.Command, args []string) error {
		devices, err := device.EnumerateDevices()
		if err != nil {
			return fmt.Errorf("enumerate devices: %w", err)
		}

		if len(devices) == 0 {
			return fmt.Errorf("no AUKEY KM-G15 device found")
		}

		fmt.Printf("Found %d interface(s):\n\n", len(devices))
		for i, d := range devices {
			fmt.Printf("Interface %d:\n", i)
			fmt.Printf("  VID: 0x%04X\n", d.VendorID)
			fmt.Printf("  PID: 0x%04X\n", d.ProductID)
			fmt.Printf("  Product: %s\n", d.ProductString)
			fmt.Printf("  Manufacturer: %s\n", d.ManufacturerString)
			fmt.Printf("  Usage Page: 0x%04X\n", d.UsagePage)
			fmt.Printf("  Usage: 0x%04X\n", d.Usage)
			fmt.Println()
		}
		return nil
	},
}

func init() {
	rootCmd.AddCommand(infoCmd)
}
