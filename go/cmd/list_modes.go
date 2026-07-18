package cmd

import (
	"fmt"

	"github.com/spf13/cobra"

	"github.com/ffexis/aukey-km-g15-rgb/internal/effects"
)

var listModesCmd = &cobra.Command{
	Use:   "list-modes",
	Short: "List available lighting modes",
	RunE: func(cmd *cobra.Command, args []string) error {
		fmt.Println("Available lighting modes:\n")
		fmt.Println("ID | Chinese Name   | English Name")
		fmt.Println("---|----------------|------------------")

		for _, m := range effects.ListModes() {
			fmt.Printf("%2d | %-14s | %s\n", m.ID, m.NameCN, m.NameEN)
		}
		return nil
	},
}

func init() {
	rootCmd.AddCommand(listModesCmd)
}
