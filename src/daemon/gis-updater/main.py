import sys
import time
import requests

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10

def get_country_gis(codes):
    """using https://restcountries.com/#rest-countries"""
    query = list(map(lambda x: "{" + x + "}", codes))
    query = ','.join(str(x) for x in query)
    try:
        return requests.get(f"https://restcountries.com/v3.1/alpha?codes={query}").json()
    except Exception as e:
        return e

def update_entitie(id, latlong):

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis to retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        data = requests.get(f"http://0.0.0.0:20002/api/without_coordinates?limit={ENTITIES_PER_ITERATION}").json()
        if data:
            for ent in data:
                lat_long = get_country_gis(ent['country'])


        # !TODO: 2- Use the entity information to retrieve coordinates from an external API
        # !TODO: 3- Submit the changes
        time.sleep(POLLING_FREQ)
