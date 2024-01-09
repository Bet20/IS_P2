package main

import (
	"fmt"
	"migrator/consumer"
	"migrator/db"

	// "migrator/db"
	// "os"
	"time"
)

const (
	VERSION       = "0.0.1"
	MIGRATOR_TICK = time.Second * 10
)

func main() {
	fmt.Printf("running Migrator (version %s)", VERSION)
	// args := os.Args
	// if len(args) > 1 {
	// 	documentId := args[1]

	// 	document := db.GetDocument(documentId)
	// 	db.AddDocumentToRelationalDatabase(document)
	// 	return
	// }

	for range time.Tick(MIGRATOR_TICK) {
		fmt.Printf("MIGRATOR TICK")
    fmt.Printf("%v", db.GetAllDocuments())
		consumer.Consume()
	}
}
