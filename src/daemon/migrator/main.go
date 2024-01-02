package main

import (
	"fmt"
	"migrator/consumer"
	"migrator/db"
	"os"
  "time"
)

const (
	VERSION = "0.0.1"
  MIGRATOR_TICK = 60
)

func main() {
	fmt.Printf("running Migrator (version %s\n)", VERSION)
	args := os.Args
	if len(args) > 1 {
		documentId := args[1]

		document := db.GetDocument(documentId)
		db.AddDocumentToRelationalDatabase(document)
		return
	}
	
	consumer.Consume()
}
