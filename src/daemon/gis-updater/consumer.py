import pika
import signal
import os
import json
import requests
import psycopg2

CONN_STRING = "host='db-rel' dbname='is' user='is' password='is'"

edge_cases = {
	'uk': 'united kingdom',
	'us': 'united states',
}

def get_country_gis(name):
    """using https://restcountries.com/#rest-countries"""

    try:
        return requests.get(f"https://restcountries.com/v3.1/name/{name}").json()
    except Exception as e:
        return None

def lower_and_fix_edge_cases(countries):
    return list(map(lambda country: edge_cases.get(country) if edge_cases.get(country) else country.lower(), countries))

def update_entity(id, lat, long):
    conn = psycopg2.connect(CONN_STRING)
    cursor = conn.cursor()
    query = """
INSERT INTO public.countries (name, geom)
               VALUES   (%s, 'POINT(%s %s)')
               ON CONFLICT (name) DO NOTHING"""
    cursor.execute(query, (id, lat, long, ))
    conn.commit()

    cursor.close()
    conn.close()

def callback(ch, method, properties, body):
    try:
        b = json.loads(body)
        countries = b.get('countries')
        countries = lower_and_fix_edge_cases(countries)
        print("countries: ", countries)
        for country in countries:
            try:
                data = get_country_gis(country)

                if not data:
                    break

                for d in data:

                    lat = d.get('latlng')[0]
                    long = d.get('latlng')[1]
                    name = d.get('name').get('common') if d.get('name').get('common') else country
                    update_entity(name, lat, long)
            except Exception as e:
                print(f"failed to insert {country} into db: ", e)
                continue

        print("****** Gis-Updater is updating GIS data ******")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Service GIS-UPDATER Error: ", e)
        return

def consume():
    try:
        user, password, vhost = 'is', 'is', 'is'
        credentials = pika.PlainCredentials(user, password)

        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, vhost, credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange='preference_exchange', exchange_type='direct', durable=True)
        result = channel.queue_declare(queue='service_gis_updater', exclusive=False)
        queue_name = result.method.queue

        channel.queue_bind(exchange='preference_exchange', queue=queue_name, routing_key='high_priority')

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        print("Service GIS-UPDATER Waiting for messages. To exit, press CTRL+C")

        def exit_handler(signum, frame):
            print("Service GIS-UPDATER Exiting...")
            connection.close()
            return

        signal.signal(signal.SIGINT, exit_handler)
        signal.signal(signal.SIGTERM, exit_handler)

        channel.start_consuming()
    except Exception as e:
        print("Service GIS-UPDATER Error: ", e)
        return
