import json
import time
from time import time
from confluent_kafka import Consumer
from confluent_kafka.admin import AdminClient, NewTopic

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'topic_1'


c = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe([KAFKA_TOPIC])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received message: {}'.format(msg.value().decode('utf-8')))

c.close()
