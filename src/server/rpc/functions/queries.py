import psycopg2

USER = "is"
PASSWORD = "is"
HOST = "is-db"
PORT = "5432"
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
                                      port=PORT,
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
    return execute_query(xml_table_prefix + " SELECT xpath('/Discogs/Releases/Release', file) FROM tbl", fetch=True)

def all_release_titles():
    return execute_query(xml_table_prefix + " SELECT xpath('/Discogs/Releases/Release/Title/text()', file) FROM tbl", fetch=True)

def count_releases():
    return execute_query(xml_table_prefix + "SELECT count ( SELECT xpath('/discogs/releases/Release', file) FROM tbl )", fetch=True)



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

def all_labels():
    return execute_query(xml_table_prefix + "SELECT xpath('/Discogs/labels/label/name/text()', file) FROM tbl", fetch=True)

def label_by_id(label_id):
    return execute_query(xml_table_prefix + "SELECT xpath('/discogs/labels/label[@id=%s]/name/text()', file) FROM tbl", (label_id,), fetch=True)

def label_by_name(label_name):
    return execute_query(xml_table_prefix + "SELECT xpath('/discogs/labels/label[name=%s]/name/text()', file) FROM tbl", (label_name,), fetch=True)

# Simple count queries, TODO: Write more nuanced counting queries

def count_releases():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Release)', file) FROM tbl", fetch=True)

def count_labels():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Artist)', file) FROM tbl", fetch=True)

def count_artists():
    return execute_query(xml_table_prefix + "SELECT xpath('count(//Label)', file) FROM tbl", fetch=True)

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

def soft_delete_document(document_name):
    return execute_query("delete_document(%s)", (document_name,), fetch=False)


