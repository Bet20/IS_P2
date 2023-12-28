package main

import (
	"fmt"
	"reflect"
	"strconv"
	"time"
	"watcher/db"
	"watcher/message"

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

func watch(importedDocuments []db.ImportedDocument) (int, []db.ImportedDocument) {
	newImportedDocuments := db.ImportedDocuments()
	if reflect.DeepEqual(newImportedDocuments, importedDocuments) {
		return -1, newImportedDocuments
	}

	for _, newDoc := range newImportedDocuments {
		exists := false
		for _, oldDoc := range newImportedDocuments {
			if newDoc.Filename == oldDoc.Filename {
				exists = true
				break
			}
		}

		if !exists {
			return newDoc.Id, newImportedDocuments
		}
	}
	return -1, newImportedDocuments
}

func main() {
	fmt.Printf("Running Watcher daemon version %s", VERSION)
	newDocumentId, importedDocuments := watch(nil)
	message.Send(strconv.Itoa(newDocumentId))

	for range time.Tick(WATCHER_TICK) {
		func() {
			fmt.Printf("Checking db for changes...")
			newDocumentId, newDocuments := watch(importedDocuments)
			if newDocumentId != -1 {
				message.Send(strconv.Itoa(newDocumentId))
				// TODO: Changed
				fmt.Println("There have been changes made to imported_documents")
			} else {
				importedDocuments = newDocuments
				fmt.Println("No changes were found...")
			}
		}()
	}
}
