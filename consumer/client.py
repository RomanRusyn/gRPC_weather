import grpc

# import the generated classes
import weather_pb2
import weather_pb2_grpc


# # open a gRPC channel
# channel = grpc.insecure_channel('localhost:50051')
#
# # create a stub (client)
# stub = weather_pb2_grpc.WeatherAppStub(channel)
#
# # create a valid request message
# name = input("Please enter the city: ")
# city = weather_pb2.City(name=name)
# print(f"city = {city}")
#
# response = stub.GetWeather(city)
# print(response)

def run():
    host = 'localhost'
    port = 1449
    with open('/home/roman/server.crt', 'rb') as f:  # path to my cert location
        trusted_certs = f.read()
    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    # channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)
    with grpc.secure_channel('{}:{}'.format(host, port),
                             credentials) as channel:
    # with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherAppStub(channel)
        name = input("Please enter the city: ")
        city = weather_pb2.City(name=name)
        response = stub.GetWeather(city)
        print(f"Greeter client received: {response}")


if __name__ == '__main__':
    # logging.basicConfig()
    run()
