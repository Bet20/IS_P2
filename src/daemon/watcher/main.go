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

	updatedImportedDocuments := importedDocuments
	newImportedDocuments := db.ImportedDocuments()

	printImportedDocuments(updatedImportedDocuments)
	printImportedDocuments(newImportedDocuments)

	if reflect.DeepEqual(newImportedDocuments, importedDocuments) {
		println("DOCUMENTS ARE DeeplyEqual")
		return -1, importedDocuments
	}

	for i, newDoc := range newImportedDocuments {
		exists := false
		for _, oldDoc := range importedDocuments {
			if newDoc.Filename == oldDoc.Filename {
				exists = true
				break
			}
		}

		if !exists {
			updatedImportedDocuments = append(updatedImportedDocuments, newImportedDocuments[i])
			return newDoc.Id, updatedImportedDocuments
		}
	}

	return -1, importedDocuments
}

func main() {
	fmt.Printf("Running Watcher daemon version %s", VERSION)
	_, importedDocuments := watch(nil)

	for range time.Tick(WATCHER_TICK) {
		func() {
			fmt.Printf("Checking db for changes...")
			newDocumentId, newDocuments := watch(importedDocuments)
			if newDocumentId != -1 {
				// Create set out of countries
				fmt.Printf("There have been changes made to imported_documents %d\n", (newDocumentId))
				message.Send(strconv.Itoa(newDocumentId), db.GetCountriesFromDocument(strconv.Itoa(newDocumentId)))
				importedDocuments = newDocuments
			} else {
				fmt.Println("No changes were found...")
			}
		}()
	}
}
