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

# def get_all_documents():
#     data = execute_query(
#         """
#             SELECT
#             json_build_object(
#             'id', json_agg(id),
#             'title', json_agg(file_name)
#             )
#             FROM imported_documents;
# """)

#     return json.dumps(data[0][0])

@app.route('/api/releases_options', methods=['GET'])
def get_documents_ids():
    data = execute_query(
        """
            SELECT id FROM imported_documents;
""")
    return list(map(lambda x: x[0], data))

if __name__ == '__main__':
    print("Starting API...")
    app.run(host="0.0.0.0", port=PORT)