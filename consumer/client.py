import grpc

# import the generated classes
import consumer.weather_pb2
import consumer.weather_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = weather_pb2_grpc.WeatherAppStub(channel)

# create a valid request message
city = weather_pb2.City(name="Rivne")
print(f"city = {city}")
print(f"stub-{stub}")
# weather = weather_pb2.Weather(conditions="cloudy",temp=12,humidity=222,
#                               pressure=1080,timestamp=1242335)

# make the call
# response = stub.GetWeather(city)
# response = weather_pb2.CityWeather()
# stub.GetWeather(city)
response = stub.GetWeather(weather_pb2.City(name='Rivne'))
print(f"citiweather_client: {type(response)}")
print(f"citiweather_client: {type(weather_pb2.Weather)}")
print(f"citiweather_client: {type(response.weather)}")
print(f"citiweather_client type is: {type(weather_pb2.CityWeather())}")


print(response)
