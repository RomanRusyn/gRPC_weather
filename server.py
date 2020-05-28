import grpc
from concurrent import futures
import time

# import the generated classes
import weather_pb2
import weather_pb2_grpc

# import the original consumer.py
import consumer

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

        # text = request_weather.replace('\n', '').replace('\r', '')
        # words = text.split(' ')
        # keywords = self.keywords(words)

        response = CityWeather()
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




if __name__== "__main__":
    serve()
