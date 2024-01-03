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
	Id         int
	Filename   string
	Created_on string
	Updated_on string
	Deleted_on string
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

		err := documents.Scan(&document.Id, &document.Filename, &document.Created_on, &document.Updated_on, &document.Deleted_on)
		utils.E(err)

		imported_documents = append(imported_documents, document)
	}

	documents.Close()
	conn.Close()
	return imported_documents
}

func GetCountriesFromDocument(documentId string) []string {
	conn, err := sql.Open("postgres", CONNECTION_STR_XML)
	utils.E(err, fmt.Sprintf("connectionString: %s produced error", CONNECTION_STR_XML))

	if conn.Ping() != nil {
		panic("Can't ping")
	}
	if conn == nil {
		panic("Connection is nil")
	}

	rows, err := conn.Query(`with tbl(file) as (SELECT xml FROM imported_documents where id = $1)
    SELECT xpath('/Discogs/Releases/Release/Country/text()', file) FROM tbl;`, documentId)

	utils.E(err)
	countries := []string{}
	for rows.Next() {
		var country string
		err := rows.Scan(&country)
		utils.E(err)
		fmt.Println(country)
		countries = append(countries, country)
	}

	rows.Close()
	conn.Close()
	return countries
}

func (doc *ImportedDocument) Print() {
	fmt.Printf("%d: %s\n", doc.Id, doc.Filename)
}
