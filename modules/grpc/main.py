import logging
import time
from concurrent import futures
from json import dumps
import grpc
import location_pb2
import location_pb2_grpc
import os
from kafka import KafkaProducer


TOPIC_NAME = "locations"
KAFKA_SERVERS = os.getenv("KAFKA_SERVER", "localhost:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVERS.split(','),
    api_version=(0, 11, 15),
    value_serializer=lambda v: dumps(v).encode('utf-8')
)


class LocationService(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("received")
        location = {
            "person_id": request.person_id,
            "latitude": request.latitude,
            "longitude": request.longitude
        }
        producer.send(TOPIC_NAME, location)
        producer.flush()
        return location_pb2.LocationMessage(**location)


logging.basicConfig()

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
location_pb2_grpc.add_LocationServiceServicer_to_server(
    LocationService(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
