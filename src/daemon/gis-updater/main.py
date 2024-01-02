import sys
import time
import requests
import psycopg2

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10
CONN_STRING = "host='db-rel' dbname='is' user='is' password='is'"

def get_country_gis(codes):
    """using https://restcountries.com/#rest-countries"""
    query = list(map(lambda x: "{" + x + "}", codes))
    query = ','.join(str(x) for x in query)
    try:
        return requests.get(f"https://restcountries.com/v3.1/alpha?codes={query}").json()
    except Exception as e:
        return e

def update_entity(id, latlong):
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = "UPDATE releases SET has_geolocation = true, lat = %, long = % WHERE id = %"
    lat = latlong[0]
    long = latlong[1]

    cursor.execute(query, (lat, long, id, ))
    records = cursor.fetchall()

 

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # data = requests.get(f"http://0.0.0.0:20002/api/without_coordinates?limit={ENTITIES_PER_ITERATION}").json()
        data = []
        if data:
            for ent in data:
                country = ent.get('country')
                if country:
                    lat_long = get_country_gis(ent['country'])

        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)
