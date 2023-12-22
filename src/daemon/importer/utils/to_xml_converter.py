import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET

from reader import CSVReader
from entities.Label import Label
from entities.Release import Release
from entities.Artist import Artist

class CSVtoXMLConverter:
    def __init__(self, path):
        self._reader = CSVReader(path)
        self._labels_dict = {}
        self._artists_dict = {}

    def get_or_create_label(self, row):
        label_id = row["label_id"]
        if label_id not in self._labels_dict:
            label = Label(row["label_id"], row["label_name"], row["company_name"])
            self._labels_dict[label_id] = label
        return self._labels_dict[label_id]

    def get_or_create_artist(self, row):
        artist_id = row["artist_id"]
        if artist_id not in self._artists_dict:
            artist = Artist(row["artist_id"], row["artist_name"])
            self._artists_dict[artist_id] = artist
        return self._artists_dict[artist_id]

    def to_xml(self):
        releases = self._reader.read_entities(
            attr="release_id",
            builder=lambda row: Release(
                original_id=row["release_id"],
                title=row["title"],
                status=row["status"],
                year=row["release_date"],
                genre=row["genre"],
                style=row["style"],
                notes=row["notes"],
                country=row["country"]
            ),
        )

        def after_creating_label(label, row):
            releases[row['release_id']].add_label(label)

        labels = self._reader.read_entities(
            attr="label_id",
            builder=lambda row: self.get_or_create_label(row),
            after_create=after_creating_label
        )

        def after_creating_artist(artist, row):
            releases[row['release_id']].add_artist(artist)

        artists = self._reader.read_entities(
            attr="artist_id",
            builder=lambda row: self.get_or_create_artist(row),
            after_create=after_creating_artist
        )

        # generate the final xml
        root_el = ET.Element("Discogs")

        releases_el = ET.Element("Releases")
        labels_el = ET.Element("Labels")
        artists_el = ET.Element("Artists")

        for value in labels.values():
            labels_el.append(value.to_xml())

        for value in artists.values():
            artists_el.append(value.to_xml())

        for release in releases.values():
            releases_el.append(release.to_xml())

        root_el.append(releases_el)
        root_el.append(labels_el)
        root_el.append(artists_el)

        return root_el

    def to_xml_str(self):
        data = self.to_xml()
        if data is not None:
            xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
            dom = md.parseString(xml_str)
            return dom.toprettyxml()
