package db

import (
	"database/sql"
	"fmt"
	"watcher/utils"

	_ "github.com/lib/pq"
)

const (
	CONNECTION_STR_XML = "user=is password=is dbname=is host=db-xml sslmode=disable"
)

type ImportedDocument struct {
	id         int
	filename   string
	created_on string
	updated_on string
	deleted_on string
}

// Returns the imported_documents from the db-xml.
// It returns them in an ImportedDocument structure
// to better compare which of them are persistent and
// which are not
func ImportedDocuments() []ImportedDocument {
	var imported_documents []ImportedDocument

	conn, err := sql.Open("postgres", CONNECTION_STR_XML)
	utils.E(err, fmt.Sprintf("connectionString: %s produced error", CONNECTION_STR_XML))

	if conn.Ping() != nil {
    // TODO: Should have a recovery method
		panic("Can't ping")
	}

	if conn == nil {
		panic("Connection is nil")
	}

	documents, err := conn.Query("SELECT id, file_name, created_on, updated_on, deleted_on FROM imported_documents;")
	utils.E(err)

	for documents.Next() {
		var document ImportedDocument

		err := documents.Scan(&document.id, &document.filename, &document.created_on, &document.updated_on, &document.deleted_on)
		utils.E(err)

		imported_documents = append(imported_documents, document)
	}

	documents.Close()
	conn.Close()
	return imported_documents
}

func (doc *ImportedDocument) Print() {
	fmt.Printf("%d: %s\n", doc.id, doc.filename)
}
