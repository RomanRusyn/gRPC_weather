""""Script for getting, decoding, logging data from kafka server"""
import json
import logging

import pandas as pd
from confluent_kafka import Consumer
from threading import Thread


class ConsumerClass(object):
    def __init__(self):
        self._should_stop = False
        self.c = Consumer({
            'bootstrap.servers': 'localhost:29092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        })
        self.c.subscribe(['weatherForToday'])
        self._city_weather = {}
        self.thread = Thread(target=self.get_weather)
        self.thread.start()


    def __del__(self):
        print("die ConsumerClass")

    def get(self, city):
        print(f"len of city dict: {len(self._city_weather)}")
        print(f"city in request : {city}")
        return self._city_weather.get(city, [])

    def get_weather(self):
        count = 0
        while not self._should_stop:
            msg = self.c.poll(1.0)

            if msg is None:
                # print("message is none")
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            logging.basicConfig(filename='consumer_results.log', filemode='w',
                                datefmt='%d-%b-%y %H:%M:%S',
                                level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s '
                                       '- %(message)s')

            city = msg.key().decode('utf-8')
            conditions = json.loads(msg.value().decode('utf-8'))
            self._city_weather = {city: conditions}

            result_list = []
            result_list.append(self._city_weather)
            data = {'city': [], 'conditions': [], 'temp': [], 'humidity': [],
                    'pressure': []}
            for dict in result_list:
                for key, value in dict.items():
                    data['city'].append(key)
                    # print(key)
                    for v_key, v_value in value.items():
                        data[v_key].append(v_value)
                        # print(v_key, v_value)

            new_data = pd.DataFrame(data=data)
            # print(new_data)

            logging.info('Town: {}'.format(city))
            logging.info(
                'Conditions: {}'.format(conditions))
            count += 1
            if count < 100:
                continue
            else:
                self._should_stop = True
        self.c.close()
