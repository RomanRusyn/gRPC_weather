import concurrent.futures
import time
from concurrent import futures
from threading import Thread

import consumer
import grpc
import weather_pb2
import weather_pb2_grpc

from gRPC_weather.config import port_grpc

consumer_weather = consumer.ConsumerClass()


class WeatherAppServicer(weather_pb2_grpc.WeatherAppServicer):
    """
    The class is to define the server functions, derived from
    weather_pb2_grpc.WeatherAppServicer

    """

    def GetWeather(self, request, context):
        """Function to process received data from consumer, client and return
        response to client

        :request_weather: name of the city where client wants to see the
            weather
        :retreived_weather: dictionary with weather received from consumer
        :city_weather: calling function from .proto file means message weather
        """
        request_weather = request.name
        w_l = []

        retreived_weather = consumer_weather.get(request_weather)
        city_weather = weather_pb2.CityWeather()
        weather = city_weather.weather.add()
        weather.conditions = retreived_weather[-1]['conditions']
        weather.temp = retreived_weather[-1]['temp']
        weather.humidity = retreived_weather[-1]['humidity']
        weather.pressure = retreived_weather[-1]['pressure']
        weather.timestamp = retreived_weather[-1]['timestamp']

        weather1 = city_weather.weather.add()
        weather1.conditions = retreived_weather[0]['conditions']
        weather1.temp = retreived_weather[0]['temp']
        weather1.humidity = retreived_weather[0]['humidity']
        weather1.pressure = retreived_weather[0]['pressure']
        weather1.timestamp = retreived_weather[0]['timestamp']

        city = weather_pb2.City(name=request_weather)

        response = weather_pb2.CityWeather(city=city, weather=[weather,weather1])
        print(f"response is: {response}")

        return response


def serve():
    """Creates the server
    :server: creates a gRPC server
    :weather_pb2_grpc.add_WeatherAppServicer_to_server(
    WeatherAppServicer(), server): use the generated function
        `add_WeatherAppServicer_to_server` to add the defined class
        to the server

    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    weather_pb2_grpc.add_WeatherAppServicer_to_server(
        WeatherAppServicer(), server)

    print(f'Starting server. Listening on port {port_grpc[-5:]}.')
    server.add_insecure_port(port_grpc)

    server.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
