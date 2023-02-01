import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.LocationMessage(
    id= 20,
    person_id = 2,
    longitude="12586.3257",
    latitude="50985.545",
    creation_time="1972-01-01T10:00:20.021Z"
        
)


response = stub.Create(location)
