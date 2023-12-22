package utils

import "fmt"

// Simple error handling function that panics on error.
// Optionaly it can print messages provided as the second
// and so forth arguments
func E(err error, messages ...string) {
	if err != nil {
		for _, msg := range messages {
			fmt.Printf("%s\n", msg)
		}
		fmt.Errorf("%s\n", err)
	}
}
