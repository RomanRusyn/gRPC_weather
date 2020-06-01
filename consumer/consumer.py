""""Script for getting, decoding, logging data from kafka server"""
import json
import logging

import pandas as pd
from confluent_kafka import Consumer



class ConsumerClass(object):
    def __init__(self):
        self.c = Consumer({
            'bootstrap.servers': 'localhost:29092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        })
        self.c.subscribe(['weatherForToday'])
        self.result_sictionary={}

    def get_weather(self):


        while True:
            msg = self.c.poll(1.0)

            if msg is None:
                print("message is none")
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
            result_sictionary = {city: conditions}
            result_list = []
            result_list.append(result_sictionary)
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
            print(new_data)

            logging.info('Town: {}'.format(city))
            logging.info(
                'Conditions: {}'.format(conditions))
        c.close()

if __name__ == '__main__':
    cons=ConsumerClass()
    cons.get_weather()