package entities

type Discogs struct {
	Artists  []Artist  `xml:"Artists>Artist"`
	Releases []Release `xml:"Releases>Release"`
	Labels   []Label   `xml:"Labels>Label"`
}

type Artist struct {
	Id         int    `xml:"id,attr"`
	OriginalId string `xml:"originalId,attr"`
	Name       string `xml:"Name"`
}

type Release struct {
	Id         int    `xml:"id,attr"`
	OriginalId string `xml:"originalId,attr"`
	Title      string `xml:"Title"`
	Status     string `xml:"Status"`
	Year       string `xml:"Year"`
	Genre      string `xml:"Genre"`
	Style      string `xml:"Style"`
	Country    string `xml:"Country"`
	Notes      string `xml:"Notes"`
}

type Label struct {
	Id          int    `xml:"id,attr"`
	OriginalId  string `xml:"originalId"`
	Name        string `xml:"Name"`
	CompanyName string `xml:"CompanyName"`
}

func NewArtist(id int, originalId string, name string) Artist {
	return Artist{id, originalId, name}
}

func NewRelease(id int, originalId string, title string, status string, year string, genre string, style string, country string, notes string) Release {
	return Release{id, originalId, title, status, year, genre, style, country, notes}
}

func NewLabel(id int, originalId string, name string, companyName string) Label {
	return Label{id, originalId, name, companyName}
}

func (discogs *Discogs) Print() {
	for _, artist := range discogs.Artists {
		artist.Print()
	}

	for _, release := range discogs.Releases {
		release.Print()
	}

	for _, label := range discogs.Labels {
		label.Print()
	}
}

func (artist *Artist) Print() {
	println("Artist:")
	println("Id: ", artist.Id)
	println("OriginalId: ", artist.OriginalId)
	println("Name: ", artist.Name)
}

func (release *Release) Print() {
	println("Release:")
	println("Id: ", release.Id)
	println("OriginalId: ", release.OriginalId)
	println("Title: ", release.Title)
	println("Status: ", release.Status)
	println("Year: ", release.Year)
	println("Genre: ", release.Genre)
	println("Style: ", release.Style)
	println("Country: ", release.Country)
	println("Notes: ", release.Notes)
}

func (label *Label) Print() {
	println("Label:")
	println("Id: ", label.Id)
	println("OriginalId: ", label.OriginalId)
	println("Name: ", label.Name)
	println("CompanyName: ", label.CompanyName)
}
