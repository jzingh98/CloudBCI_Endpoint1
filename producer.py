import json
import time
from time import time, sleep
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'topic_1'

# admin_client = AdminClient({
#     "bootstrap.servers": 'localhost:9092'
# })
#
# topic_list = [NewTopic("topic_1", 1, 1)]
# admin_client.create_topics(topic_list)

producer = Producer({
    'bootstrap.servers': KAFKA_BROKER,
    'socket.timeout.ms': 100,
    'api.version.request': 'false',
    'broker.version.fallback': '0.9.0',
    'message.max.bytes': 1000000000
})


def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(
            msg.topic(), msg.partition()))


def send_msg_async(msg):
    print("Sending message")
    try:
        msg_json_str = str({"data": json.dumps(msg)})
        producer.produce(
            KAFKA_TOPIC,
            msg_json_str,
            callback=lambda err, original_msg=msg_json_str: delivery_report(err, original_msg
                                                                            ),
        )
        producer.flush()
    except Exception as ex:
        print("Error : ", ex)


def main():
    start_time = int(time() * 1000)
    data = {"name": "jag", "email": "email.com"}

    send_msg_async(data)

    end_time = int(time() * 1000)
    time_taken = (end_time - start_time) / 1000
    print("Time taken to complete = %s seconds" % (time_taken))



for i in range(5):
    main()
    sleep(1)
