import logging

from confluent_kafka import Consumer

log = logging.basicConfig(filename='consumer_results.log', filemode='w',
                          datefmt='%d-%b-%y %H:%M:%S',
                          level=logging.INFO,
                          format='%(asctime)s - %(name)s - %(levelname)s '
                                 '- %(message)s')

consumer_c = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

port_grpc = '[::]:50051'
