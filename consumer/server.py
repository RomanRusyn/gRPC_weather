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



# create a class to define the server functions, derived from
# weather_pb2_grpc.CalculatorServicer
consumer_weather = consumer.ConsumerClass()

thread2 = Thread(target=consumer_weather.get_weather)
thread2.start()
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
              f"{consumer_weather.get_dict('Rivne')}")
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

# def main():

thread1 = Thread(target=serve)
thread1.start()

    # thread1.join()
    # thread2.join()
# if __name__ == "__main__":
#     main()
    # print(f"res_dict->{res_dict}")
    # serve()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     consumer_weather = consumer.ConsumerClass()
    #     serve_finc = executor.submit(serve(), )
    #     serve_finc.sleep
    #
    #     my_f = executor.submit(consumer_weather.get_weather(),)
    #     res_dict = my_f.result_sictionary
    #     print(f"res_dict after executor->{res_dict}")
    #     time.sleep(2)
