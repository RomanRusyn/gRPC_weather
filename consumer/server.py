import time
from concurrent import futures
import concurrent.futures

# import the original consumer.py
import consumer
import grpc
# import the generated classes
import weather_pb2
import weather_pb2_grpc
from threading import Thread


consumer_weather = consumer.ConsumerClass()
print(f"consumer weather-> {consumer_weather}")
# create a class to define the server functions, derived from
# weather_pb2_grpc.CalculatorServicer

class WeatherAppServicer(weather_pb2_grpc.WeatherAppServicer):

    def GetWeather(self, request, context):
        request_weather = request.name
        print(f"request_weather from GetWeather = {request_weather}")
        cityweather = weather_pb2.CityWeather()
        weather = cityweather.weather.add()
        weather.conditions="conditions"
        weather.temp = 12
        weather.humidity = 123
        weather.pressure = 1080
        weather.timestamp = 1234456
        city = weather_pb2.City(name="Rivne")
        print(f"from consumer_weather-> "
              f"{consumer_weather.get('Rivne')}")
        #     cityweather = weather_pb2.CityWeather()
        #     weather = cityweather.weather.add()
        #     weather.conditions="conditions"
        #     weather.temp = 12
        #     weather.humidity = 123
        #     weather.pressure = 1080
        #     weather.timestamp = 1234456
        #     city = weather_pb2.City(name=res_dict.key())
        response = weather_pb2.CityWeather(city=city, weather=[weather])
        print(f"response is: {response}")

        return response


def serve():
    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # use the generated function `add_WeatherAppServicer_to_server`
    # to add the defined class to the server
    weather_pb2_grpc.add_WeatherAppServicer_to_server(
        WeatherAppServicer(), server)

    # listen on port 50051

    print('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')

    server.start()
    # for i in range(100):
    #     print(i)
    #     time.sleep(2)
    #     print(f"i after sleep{i*i}")

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
