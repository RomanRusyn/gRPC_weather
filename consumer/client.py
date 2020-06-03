import grpc

# import the generated classes
import weather_pb2
import weather_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = weather_pb2_grpc.WeatherAppStub(channel)

# create a valid request message
name = input("Please enter the city: ")
city = weather_pb2.City(name=name)
print(f"city = {city}")

response = stub.GetWeather(city)
print(response)
