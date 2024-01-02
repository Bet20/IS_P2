import sys
import psycopg2

from flask import Flask, request
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000
CONN_STRING = "host='db-rel' dbname='is' user='is' password='is'"


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

@app.route('/api/without_coordinates', methods=['GET'])
def get_entities_without_coordinates():
    args = request.args
    limit = args['limit']
    print(limit)

    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    cursor.execute("SELECT id, country FROM releases WHERE country IS NOT NULL LIMIT %s", (limit, ))
    records = cursor.fetchall()
    return records

@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("""SELECT
                   r.id,
  r.title,
  r.year,
  r.genre,
  ST_X(ST_AsGeoJSON(c.geom)::geometry) AS longitude,
  ST_Y(ST_AsGeoJSON(c.geom)::geometry) AS latitude
FROM
  public.releases r
JOIN
  public.countries c ON r.country = c.id
LIMIT 1000;""")
    
    # Fetch the result
    releases = cursor.fetchall()

    # Convert the result into the desired format
    markers = [
        {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {
                "id": id,
                "title": title,
                "year": year,
                "genre": genre,
                "imgUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Discogs_record_icon.svg/1200px-Discogs_record_icon.svg.png",
            }
        }
        for id, title, year, genre, latitude, longitude in releases
    ]

    cursor.close()
    conn.close()

    return markers

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
