import time
from concurrent import futures

# import the original consumer.py
import consumer
import grpc
# import the generated classes
import weather_pb2
import weather_pb2_grpc


# import test_consumer

# create a class to define the server functions, derived from
# weather_pb2_grpc.CalculatorServicer
class WeatherAppServicer(weather_pb2_grpc.WeatherAppServicer):

    # calculator.square_root is exposed here
    # the request and response are of the data type
    # calculator_pb2.Number

    # def SquareRoot(self, request, context):
    #     response = weather_pb2.City()
    #     response.value = reqowm.main(request.value)
    #     return response

    def GetWeather(self, request, context):
        request_weather = request.name
        print(f"request_weather from GetWeather = {request_weather}")
        print(f"reauest: {request}")

        # text = request_weather.replace('\n', '').replace('\r', '')
        # words = text.split(' ')
        # keywords = self.keywords(words)
        # weather = weather_pb2.Weather(conditions="cloudy", temp=12,
        #                               humidity=222,
        #                               pressure=1080, timestamp=1242335)
        # weather2 = weather_pb2.Weather(["cloudy", 12, 222, 1080, 1235453])
        print("_____________before weather__________-")
        cityweather1 = weather_pb2.CityWeather()
        weather1 = cityweather1.weather.add()
        weather1.conditions="conditions"
        weather1.temp = 12
        weather1.humidity = 123
        weather1.pressure = 1080
        weather1.timestamp = 1234456
        # weather3 = weather_pb2.Weather.extend(
        #     ["cloudy", 12.0, 222.9, 1080.6, 1235453])
        # w4= weather_pb2.CityWeather
        print("_________after weather------------")

        city1 = weather_pb2.City(name="Rivne")
        print("--------before response")
        # response = weather_pb2.CityWeather(city=city1, weather=weather1)
        response = weather_pb2.CityWeather(city=city1, weather=[weather1])
        # response = request_weather
        print(f"response is: {response}")
        # response.keywords.extend(keywords)

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

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
