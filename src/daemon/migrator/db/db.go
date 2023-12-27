package db

import (
	"database/sql"
	"encoding/xml"
	"fmt"
	"migrator/entities"
	"migrator/utils"

	_ "github.com/lib/pq"
)

const (
	CONNECTION_STR_XML  = "user=is password=is dbname=is host=0.0.0.0 port=10001 sslmode=disable"
	CONNECTION_STR_REL  = "user=is password=is dbname=is host=0.0.0.0 port=10002 sslmode=disable"
	INSERT_ARTIST_STMT  = "INSERT INTO artists (id, name) VALUES ($1, $2)"
	INSERT_LABEL_STMT   = "INSERT INTO labels (id, name, company_name) VALUES ($1, $2, $3)"
	INSERT_RELEASE_STMT = `INSERT INTO releases
    (id, 
    title,
    status,
    genre,
    style,
    year,
    notes,
    artist_id,
    label_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);`
)

type ImportedDocument struct {
	id         int
	filename   string
	created_on string
	updated_on string
	deleted_on string
}

func GetDocument(documentId string) entities.Discogs {
	conn, err := sql.Open("postgres", CONNECTION_STR_XML)
	utils.E(err, fmt.Sprintf("connectionString: %s produced error", CONNECTION_STR_XML))
	defer conn.Close()

	if conn.Ping() != nil {
		panic("There has been an error while pinging the database")
	}

	documents, err := conn.Query("SELECT xml FROM imported_documents WHERE id = $1;", documentId)
	utils.E(err)
	defer documents.Close()

	var discogs entities.Discogs
	for documents.Next() {
		var rawData string

		err := documents.Scan(&rawData)
		utils.E(err)

		xml.Unmarshal([]byte(rawData), &discogs)

		discogs.Print()
	}

	return discogs
}

func AddDocumentToRelationalDatabase(discogs entities.Discogs) error {
	conn, err := sql.Open("postgres", CONNECTION_STR_REL)
	utils.E(err, fmt.Sprintf("connectionString: %s produced error", CONNECTION_STR_REL))
	defer conn.Close()

	if conn.Ping() != nil {
		panic("There has been an error while pinging the database")
	}

	for _, artist := range discogs.Artists {
		_, err = conn.Exec(INSERT_ARTIST_STMT, artist.Id, artist.Name)
		utils.E(err, fmt.Sprintf("Artist relational db insert error, id: %d", artist.Id))
	}

	for _, label := range discogs.Labels {
		_, err = conn.Exec(INSERT_LABEL_STMT, label.Id, label.Name, label.CompanyName)
		utils.E(err, fmt.Sprintf("Label relational db insert error, id: %d", label.Id))
	}

	for _, release := range discogs.Releases {
		_, err = conn.Exec(INSERT_RELEASE_STMT,
			release.Id,
			release.Title,
			release.Status,
			release.Genre,
			release.Style,
			release.Year,
			release.Notes,
      release.ArtistRef,
      release.LabelRef,
		)
    utils.E(err)
	}

  fmt.Println("finished loading the selected document to the relational database")

	return nil
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
