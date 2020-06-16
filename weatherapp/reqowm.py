"""Script for parsing weather site and using kafka producer

Script takes information from "https://openweathermap.org/".
API key for Roman is "53e054d0ccc375a2b5d0b943fcb84ee5". Need key for using
sites API.
You need id of the city for accurate results, so use function get_city_id

The Example of usage:
    python reqowm.py

    Script prints weather in cities which are located in "sample_of_cities"
    tuple. Output is like:
    Weather in {city} for today is:
    conditions: light rain
    temp: 20
    humidity: 26
    pressure: 1016

"""
import json
import logging
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep
import aiohttp
import asyncio
import timeit

import requests
from confluent_kafka import Producer

APPID = "53e054d0ccc375a2b5d0b943fcb84ee5"
SAMPLE_OF_CITIES = (
    "Rivne", "Kiev", "Miami", "Reykholt", "Los Angeles", "Palapye",
    "Cloncurry", "Tokyo", "Norilsk")
TOPIC = "weatherForToday"


async def get_city_id(city_name):
    """Fucntion for returning id of the city"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.openweathermap.org/data/2.5/find",
                              params={'q': city_name, 'type': 'like',
                                      'units': 'metric', 'lang': 'en',
                                      'APPID': APPID}) as resp:
                data = await resp.json()
        # data = result.json()
        city_id = data['list'][0]['id']
    except Exception as e:
        print("Exception (find city):", e, " please write correct city")
        pass
    assert isinstance(city_id, int)
    return city_id


async def request_current_weather(city_name):
    """Function for returning weather data"""
    city_id = await get_city_id(city_name)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "http://api.openweathermap.org/data/2.5/weather",
                              params={'id': city_id, 'units': 'metric',
                                      'lang': 'en', 'APPID': APPID}) as resp:
                # result = await resp.json()

                data = await resp.json()

        result_dict = {"conditions": data['weather'][0]['description'],
                       "temp": data['main']['temp'],
                       "humidity": data['main']['humidity'],
                       "pressure": data['main']['pressure'],
                       "timestamp": str(datetime.now())
                       }
        # print(result_dict)
        return result_dict
    except Exception as e:
        print("Exception (weather):", e)
        pass


def printing_results(results):
    """Function for printing weather results into console. Its used for
    convenient, not used in development"""
    for index, result in enumerate(results):
        print(f"Weather in {SAMPLE_OF_CITIES[index]} for today is:")
        print(f"conditions: {result['conditions']}")
        print(f"temp: {result['temp']}")
        print(f"humidity: {result['humidity']}")
        print(f"pressure: {result['pressure']}")
        print(f"timestamp: {result['timestamp']}")


def kafka_producer(results):
    """Kafka producer function.

    Takes the results from mapping towns and weather and pushes it to kafka
    server and writes logs
    """
    logging.basicConfig(filename='weather_app.log', filemode='w',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s '
                               '- %(message)s')

    conf = {
        'bootstrap.servers': "localhost:29092",
        'client.id': socket.gethostname()}
    producer = Producer(conf)

    for index, result_dict in enumerate(results):
        print(SAMPLE_OF_CITIES[index])
        print(str(json.dumps(result_dict)))
        producer.produce(TOPIC, key=SAMPLE_OF_CITIES[index],
                         value=str(json.dumps(result_dict)))

        logging.info('Town: {}'.format(SAMPLE_OF_CITIES[index]))
        logging.info('Conditions: {}'.format(result_dict))

    # Wait up to 1 second for events.
    producer.poll(1)

async def match():
    l=[]
    for index, city in enumerate(SAMPLE_OF_CITIES):
        l.append(asyncio.create_task(request_current_weather(city)))
    for i in l:
        await i
    return l

def main():
    """Main function for combining together the functions of the script.

    Maps weather and towns in 5 threads
    """
    loop = asyncio.get_event_loop()
    value = loop.run_until_complete(match())
    list_with_weathers = []
    for city_weather in value:
        list_with_weathers.append(city_weather.result())
    print(f"list1 -> {list_with_weathers}")

    kafka_producer(list_with_weathers)


if __name__ == '__main__':
    print(
        f'1.AioHTTP time for 100 times :{timeit.timeit(main, number=100)}')
    # while True:
    #     # main()
    #
    #     sleep(10)
