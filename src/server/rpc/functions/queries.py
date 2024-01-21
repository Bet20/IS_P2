import psycopg2
import json

USER = "is"
PASSWORD = "is"
HOST = "db-xml"
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


def upload_file_to_db(name: str, data: str):
    try:
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="is-db",
                                      port="5432",
                                      database="is")

        cursor = connection.cursor()
        higienized = data.replace("'", "&apos;")
        cursor.execute("INSERT INTO imported_documents(file_name, xml) VALUES (%s, %s)", (name, higienized))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        return f"Failed to fetch data with {error}"

    finally:
        if connection:
            cursor.close()
            connection.close()
            return "Inserted document into database"


# --- End of auxiliary functions ---

# --- Queries ---

def files_list():
    return execute_query("SELECT (id, file_name) FROM imported_documents", fetch=True)


def all_releases():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
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

def get_genres():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(DISTINCT jsonb_build_object(
        'genre', (xpath('/Release/Genre/text()', rel))[1]::text
    )) AS results
FROM tbl,
    unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])

def get_releases_from_before_seventies():
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
            )
    ) AS results
FROM tbl,
        unnest(xpath('/Discogs/Releases/Release[Year<1970]', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])

def all_releases_from_artist(artist):
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
    
) SELECT jsonb_agg( distinct jsonb_build_object('title', (xpath('/Release/Title/text()', rel))[1]::text, 'year', (xpath('/Release/Year/text()', rel))[1]::text, 'status', (xpath('/Release/Status/text()', rel))[1]::text, 'genre', (xpath('/Release/Genre/text()', rel))[1]::text, 'style', (xpath('/Release/Style/text()', rel))[1]::text, 'country', (xpath('/Release/Country/text()', rel))[1]::text, 'artist_ref', (xpath('/Release/ArtistRef/text()', rel))[1]::text)) AS results FROM tbl, unnest(xpath('/Discogs/Releases/Release[ArtistRef=%s]', xml)) AS releases(rel);
        """, (artist,), fetch=True)

    return json.dumps(data[0][0])


def all_releases_from_genre(genre):
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'title', (xpath('/Release/Title/text()', rel))[1]::text,
            'year', (xpath('/Release/Year/text()', rel))[1]::text,
            'status', (xpath('/Release/Status/text()', rel))[1]::text,
            'genre', (xpath('/Release/Genre/text()', rel))[1]::text,
            'style', (xpath('/Release/Style/text()', rel))[1]::text,
            'country', (xpath('/Release/Country/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel)
WHERE (xpath('/Release/Genre/text()', rel))[1]::text = %s;"""
        , (genre,), fetch=True)

    return json.dumps(data[0][0])

def all_labels():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'name', (xpath('/Label/Name/text()', rel))[1]::text,
            'contact_info', (xpath('/Label/CompanyName/text()', rel))[1]::text,
          )
    ) AS results
FROM tbl,
        unnest(xpath('/Discogs/Labels/Label', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])


def all_artists():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'name', (xpath('/Artist/Name/text()', rel))[1]::text,
            )
    ) AS results
FROM tbl,
    
        unnest(xpath('/Discogs/Artists/Artist', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])

def get_countries():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)   
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'country', (xpath('/Release/Country/text()', rel))[1]::text
            )
    ) AS results
FROM tbl,
        unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])

def all_releases_from_country(country):
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'title', (xpath('/Release/Title/text()', rel))[1]::text,
            'year', (xpath('/Release/Year/text()', rel))[1]::text,
            'status', (xpath('/Release/Status/text()', rel))[1]::text,
            'genre', (xpath('/Release/Genre/text()', rel))[1]::text,
            'style', (xpath('/Release/Style/text()', rel))[1]::text,
            'country', (xpath('/Release/Country/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel)
WHERE (xpath('/Release/Country/text()', rel))[1]::text = %s;"""
        , (country,), fetch=True)

    return json.dumps(data[0][0])

def get_labels():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'id', (xpath('/Label/@id', rel))[1]::text,
            'label', (xpath('/Label/Name/text()', rel))[1]::text
            )
    ) AS results
FROM tbl,
        unnest(xpath('/Discogs/Labels/Label[position() <= 100]', xml)) AS releases(rel);"""
        , fetch=True)

    return json.dumps(data[0][0])

def all_releases_from_label(label):
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT  
    jsonb_agg(
    distinct
        jsonb_build_object(
            'title', (xpath('/Release/Title/text()', rel))[1]::text,
            'year', (xpath('/Release/Year/text()', rel))[1]::text,
            'status', (xpath('/Release/Status/text()', rel))[1]::text,
            'genre', (xpath('/Release/Genre/text()', rel))[1]::text,
            'style', (xpath('/Release/Style/text()', rel))[1]::text,
            'country', (xpath('/Release/Country/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel)
WHERE (xpath('/Release/LabelRef/text()', rel))[1]::text = %s;"""
        , (label,), fetch=True)

    return json.dumps(data[0][0])

def get_artists():
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
        DISTINCT jsonb_build_object(
            'id', (xpath('/Artist/@id', rel))[1]::text,
            'artist', (xpath('/Artist/Name/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Artists/Artist[position() <= 100]', xml)) AS releases(rel);
"""
        , fetch=True)

    return json.dumps(data[0][0])

def all_releases_from_artist(artist):
    data = execute_query(
        """WITH tbl AS (
    SELECT xml FROM imported_documents
)
SELECT
    jsonb_agg(
    distinct
        jsonb_build_object(
            'title', (xpath('/Release/Title/text()', rel))[1]::text,
            'year', (xpath('/Release/Year/text()', rel))[1]::text,
            'status', (xpath('/Release/Status/text()', rel))[1]::text,
            'genre', (xpath('/Release/Genre/text()', rel))[1]::text,
            'style', (xpath('/Release/Style/text()', rel))[1]::text,
            'country', (xpath('/Release/Country/text()', rel))[1]::text
        )
    ) AS results
FROM tbl,
     unnest(xpath('/Discogs/Releases/Release', xml)) AS releases(rel)
WHERE (xpath('/Release/ArtistRef/text()', rel))[1]::text = %s;"""
        , (artist,), fetch=True)

    return json.dumps(data[0][0])

def soft_delete_document(document_name):
    return execute_query("delete_document(%s)", (document_name,), fetch=False)
