import grpc

# import the generated classes
import weather_pb2
import weather_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = weather_pb2_grpc.WeatherAppStub(channel)

# create a valid request message
city = weather_pb2.City(value="Rivne")

# make the call
response = stub.GetWeather(city)


print(response.value)
