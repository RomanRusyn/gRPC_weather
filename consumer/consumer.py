""""Script for getting, decoding, logging data from kafka server"""
# Standard library imports
import collections
import json
import logging
from threading import Thread

# Third party imports
import pandas as pd

# Local application imports
# from gRPC_weather.config import consumer_c, log
from config_2 import consumer_c, log


class ConsumerClass(object):
    """The ConsumerClass contains

    :_consumer: connection to confluent kafka Consumer with imported
        configurations
    :_city_weather: contains dictionary with weather for chosen countries

    In a initialization moment creates a thread for reading weather from kafka

    """

    def __init__(self):
        self._should_stop = False
        self._consumer = consumer_c
        self._consumer.subscribe(['weatherForToday'])
        self._city_weather = collections.defaultdict(list)
        self.thread = Thread(target=self._retrieve_data)
        self.thread.start()

    def __del__(self):
        print("die ConsumerClass")

    def get(self, city):
        """Getting and returning weather for current city to server"""
        return self._city_weather.get(city, [])

    def pandas_printing(self, dict_for_pandas):
        """Prints weather in the cities in good looking format"""
        result_list = []
        result_list.append(dict_for_pandas)
        data = {'city': [], 'conditions': [], 'temp': [], 'humidity': [],
                'pressure': [], 'timestamp': []}
        for dict in result_list:
            for key, value in dict.items():
                data['city'].append(key)
                # print(key)
                for v_key, v_value in value.items():
                    data[v_key].append(v_value)
                    # print(v_key, v_value)

        new_data = pd.DataFrame(data=data)
        print(new_data)

    def _retrieve_data(self):
        """Queries weather in endless cycle  from kafka"""
        # count = 0
        while not self._should_stop:
            msg = self._consumer.poll(1.0)

            if msg is None:
                # print("message is none")
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            log

            city = msg.key().decode('utf-8')
            conditions = json.loads(msg.value().decode('utf-8'))
            self._city_weather[city].append(conditions)

            dict_for_pandas = {city: conditions}
            # pandas_printing(dict_for_pandas)

            logging.info('Town: {}'.format(city))
            logging.info(
                'Conditions: {}'.format(conditions))
            # count += 1
            # print(count)
            # if count > 100:
            #     self._should_stop = True
            #     self.thread.join()

        self._consumer.close()
