package main

import (
	"fmt"
	"migrator/db"
	"os"
)

const (
	VERSION = "0.0.1"
)

func main() {
	fmt.Printf("running Migrator (version %s\n)", VERSION)
	args := os.Args
	if len(args) < 2 {
		fmt.Printf("Usage: migrator [document id]\n")
		os.Exit(-1)
	}

	documentId := args[1]

	db.GetXmlDocument(documentId)
}
