package main

import (
	"fmt"
	"os"
	"reflect"
	"time"
	"watcher/db"

	_ "github.com/lib/pq"
)

const (
	WATCHER_TICK = time.Second * 60 // Check if there are changes in the DB each 5 minutes
	VERSION      = "0.0.1"
)

func printImportedDocuments(importedDocuments []db.ImportedDocument) {
	for _, doc := range importedDocuments {
		doc.Print()
	}
}

func watch(importedDocuments []db.ImportedDocument) (bool, []db.ImportedDocument) {
	newImportedDocuments := db.ImportedDocuments()
	return !reflect.DeepEqual(newImportedDocuments, importedDocuments), newImportedDocuments
}

func main() {
	fmt.Printf("Running Watcher daemon version %s", VERSION)
	_, importedDocuments := watch(nil)

	for range time.Tick(WATCHER_TICK) {
		func() {
			fmt.Printf("Checking db for changes...")
			changed, newDocuments := watch(importedDocuments)
			if changed {
				// TODO: Changed
				os.Exit(99)
			}
			importedDocuments = newDocuments

			fmt.Println("No changes were found...")
		}()
	}
}
