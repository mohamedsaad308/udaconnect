import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json
from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from kafka import KafkaProducer
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

TOPIC_NAME = "locations"
KAFKA_SERVER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    api_version=(0, 11, 15)
)


class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(
                f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")
        location = json.dumps(location).encode()
        producer.send(TOPIC_NAME, location)
        producer.flush()
        print("Sent to consumer")

        # new_location = Location()
        # new_location.person_id = location["person_id"]
        # new_location.creation_time = location["creation_time"]
        # new_location.coordinate = ST_Point(
        #     location["latitude"], location["longitude"])
        # db.session.add(new_location)
        # db.session.commit()

        return location
