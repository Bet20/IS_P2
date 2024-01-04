import sys

from flask import Flask
import psycopg2
from flask_cors import CORS
import json

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
print(PORT)

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

USER = "is"
PASSWORD = "is"
HOST = "db-xml"
DBPORT = "5432"
DATABASE = "is"

connection = None
cursor = None

# Auxiliary string to help with queries, creates a temporary table with the xml data
xml_table_prefix = "with tbl(file) as (SELECT xml FROM imported_documents)"

# --- Auxiliary functions ---
def execute_query(query, params=None, fetch=True, prefix=xml_table_prefix):
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=DBPORT,
                                      database=DATABASE)

        cursor = connection.cursor()
        cursor.execute(query, params)

        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to execute query:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

# --- End of auxiliary functions ---

# --- Queries ---

@app.route('/api/releases', methods=['GET'])
def all_releases():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents WHERE id = 1
)
SELECT
    jsonb_agg(
        jsonb_build_object(
            'title', (xpath('/Release/Title/text()', rel))[1]::text,
            'year', (xpath('/Release/Year/text()', rel))[1]::text,
            'status', (xpath('/Release/Status/text()', rel))[1]::text,
            'genre', (xpath('/Release/Genre/text()', rel))[1]::text,
            'style', (xpath('/Release/Style/text()', rel))[1]::text,
            'country', (xpath('/Release/Country/text()', rel))[1]::text,
            'artist_ref', (xpath('/Release/ArtistRef/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel);"""
        , fetch=True)
    

    return json.dumps(data[0][0])

@app.route('/api/release_titles', methods=['GET'])
def all_release_titles():
    return execute_query(xml_table_prefix + " SELECT xpath('/Discogs/Releases/Release/Title/text()', file) FROM tbl", fetch=True)


def count_releases():
    return execute_query(xml_table_prefix + "SELECT count ( SELECT xpath('/discogs/releases/Release', file) FROM tbl )", fetch=True)


@app.route('/api/artists', methods=['GET'])
def all_artists():
    return execute_query(xml_table_prefix + "SELECT xpath('/Discogs/Artists/Artist/Name/text()', file) FROM tbl", fetch=True)

def artist_name_by_id(*artist_id):
    return execute_query(xml_table_prefix + "SELECT xpath('/Discogs/Artists/Artist[@id='%s']', file) FROM tbl", (artist_id), fetch=True)


def releases_from_artist_by_name(*artist_name):
    artist_id = execute_query(xml_table_prefix + "SELECT xpath('/Discogs/Artists/Artist[Name='%s']/@id', file) FROM tbl", (artist_name), fetch=True)
    artist_id = artist_id[0][0].replace('{', '').replace('}', '')
    return execute_query(xml_table_prefix + f" SELECT xpath('//Release[ArtistRef={artist_id}]', file) FROM tbl ", (artist_id), fetch=True)


def releases_from_artist_by_id(*artist_id):
    return execute_query(xml_table_prefix + f" SELECT xpath('//Release[ArtistRef=%s]', file) FROM tbl ", (artist_id), fetch=True)

def releases_from_label_by_name(*label_name):
    label_id = execute_query(xml_table_prefix + "SELECT xpath('/Discogs/Labels/Label[Name='%s']/@id', file) FROM tbl", (label_name), fetch=True)
    label_id = label_id[0][0].replace('{', '').replace('}', '')
    return execute_query(xml_table_prefix + f" SELECT xpath('//Release[LabelRef={label_id}]', file) FROM tbl ", (label_id), fetch=True)

def releases_from_label_by_id(*label_id):
    return execute_query(xml_table_prefix + f" SELECT xpath('//Release[LabelRef=%s]', file) FROM tbl ", (label_id), fetch=True)

@app.route('/api/labels', methods=['GET'])
def all_labels():
    return execute_query(xml_table_prefix + "SELECT xpath('/Discogs/labels/label/name/text()', file) FROM tbl", fetch=True)

def label_by_id(label_id):
    return execute_query(xml_table_prefix + "SELECT xpath('/discogs/labels/label[@id=%s]/name/text()', file) FROM tbl", (label_id,), fetch=True)

def label_by_name(label_name):
    return execute_query(xml_table_prefix + "SELECT xpath('/discogs/labels/label[name=%s]/name/text()', file) FROM tbl", (label_name,), fetch=True)

# Simple count queries, TODO: Write more nuanced counting queries

@app.route('/api/count/releases', methods=['GET'])
def count_releases():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release)', file) FROM tbl", fetch=True)

@app.route('/api/count/labels', methods=['GET'])
def count_labels():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Artist)', file) FROM tbl", fetch=True)

@app.route('/api/count/artists', methods=['GET'])
def count_artists():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Label)', file) FROM tbl", fetch=True)

# Count releses from a specific label
@app.route('/api/count/releases/', methods=['GET'])
def count_releases_from_label(label):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[LabelRef=%s])', file) FROM tbl", (label,), fetch=True)

def count_releases_from_artist(artist):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[ArtistRef=%s])', file) FROM tbl", (artist,), fetch=True)

def count_releases_before_year(year):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[Year < %s])', file) FROM tbl", (year,), fetch=True)

def count_releases_after_year(year):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[Year > %s])', file) FROM tbl", (year,), fetch=True)

def count_releases_from_country(country):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[Country=%s])', file) FROM tbl", (country,), fetch=True)

def count_releases_from_genre(genre):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[contains(Genre, %s)])', file) FROM tbl", (genre,), fetch=True)

def count_releases_from_style(style):
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release[contains(Style, %s)])', file) FROM tbl", (style,), fetch=True)

if __name__ == '__main__':
    print("Starting API...")
    app.run(host="0.0.0.0", port=PORT)