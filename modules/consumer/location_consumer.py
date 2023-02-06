from kafka import KafkaConsumer
import json
from app.udaconnect.models import Location
from app import db, create_app
from geoalchemy2.functions import ST_AsText, ST_Point
import os

TOPIC_NAME = "locations"
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
consumer = KafkaConsumer(
    TOPIC_NAME,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    bootstrap_servers=[KAFKA_SERVER]
)


def write_location(location):
    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(
        location["latitude"], location["longitude"])
    db.session.add(new_location)
    db.session.commit()


with create_app().app_context():
    for location in consumer:
        location_data = location.value
        write_location(location_data)
