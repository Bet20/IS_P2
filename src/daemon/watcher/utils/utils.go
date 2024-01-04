package utils

import "fmt"

type StringSet map[string]struct{}

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

func NewStringSet(values []string) StringSet {
	set := make(StringSet)
	for _, element := range values {
		set[element] = struct{}{}
	}
	return set
}

func (s StringSet) Elements() []string {
	var elements []string
	for element := range s {
		elements = append(elements, element)
	}
	return elements
}

func (s StringSet) Print() {
	for element := range s {
		fmt.Printf("%s\n", element)
	}
}
