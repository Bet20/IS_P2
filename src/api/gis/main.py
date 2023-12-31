import sys
import psycopg2

from flask import Flask, request

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/api/without_coordinates', methods=['GET'])
def get_entities_without_coordinates():
    args = request.args
    limit = args['limit']

    conn_string = "host='db-rel' dbname='is' user='is' password='is'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id, country FROM releases WHERE has_geolocation WITH limit = %", (limit, ))
    records = cursor.fetchall()

    


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args


    return [
        {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [41.69462, -8.84679]
            },
            "properties": {
                "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
                "name": "Ronaldo",
                "country": "Portugal",
                "position": "Striker",
                "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
                "number": 7
            }
        }
    ]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
