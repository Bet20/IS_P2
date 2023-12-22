import xml.etree.ElementTree as ET
import re

from entities.Label import Label
from entities.Artist import Artist

class Release:
    _counter: int
    _label: Label = None
    _artist: Artist = None

    def __init__(self,
                 original_id: str,
                 title: str,
                 status: str,
                 year: str,
                 genre: str,
                 style: str,
                 country: str,
                 notes: str,
                 ) -> None:
        Release._counter += 1
        self._id = Release._counter
        self._original_id = original_id
        self._title = title
        self._status = status
        self._country = country
        self._style = style
        self._genre = genre
        self._notes = notes
        self._year = year

    def add_label(self, label: Label):
        self._label = label

    def add_artist(self, artist: Artist):
        self._artist = artist

    def to_xml(self):
        el = ET.Element("Release")
        el.set("id", str(self._id))
        el.set("originalId", str(self._original_id))

        title_elem = ET.Element("Title")
        title_elem.text = self._title
        el.append(title_elem)

        if self._year:
            year_elem = ET.Element("Year")
            year_elem.text = self._year
            el.append(year_elem)

        if self._status:
            status_elem = ET.Element("Status")
            status_elem.text = self._status
            el.append(status_elem)

        if self._genre:
            genre_elem = ET.Element("Genre")
            genre_elem.text = self._genre
            el.append(genre_elem)

        if self._notes:
            notes_elem = ET.Element("Notes")
            notes_elem.text = self._notes
            el.append(notes_elem)

        if self._style:
            style_elem = ET.Element("Style")
            style_elem.text = self._style
            el.append(style_elem)

        if self._country:
            country_elem = ET.Element("Country")
            country_elem.text = self._country
            el.append(country_elem)

        if self._label:
            label_elem = ET.Element("LabelRef")
            label_elem.text = str(self._label.get_id())
            el.append(label_elem)

        if self._artist:
            artist_elem = ET.Element("ArtistRef")
            artist_elem.text = str(self._artist.get_id())
            el.append(artist_elem)

        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._title}"


Release._counter = 0
