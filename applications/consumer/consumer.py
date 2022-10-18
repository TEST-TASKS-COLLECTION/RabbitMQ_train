import os 
import sys

import json

from dotenv import load_dotenv

import time
load_dotenv()

from pika import BlockingConnection, ConnectionParameters

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT= int(os.getenv("RABBIT_PORT", "5671"))
RABBIT_USERNAME= os.getenv("RABBIT_USERNAME", "guest")
RABBIT_PASSWORD= os.getenv("RABBIT_PASSWORD", "guest")

print("*"*20)
print("connecting to host", RABBIT_HOST, RABBIT_PORT, "consumer")
print("*"*20)


def main():
    print(RABBIT_HOST, RABBIT_PORT, "in consumer main")
    connection = BlockingConnection(ConnectionParameters(
                    host=RABBIT_HOST, port=RABBIT_PORT,  # type: ignore
                    ))

    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    
    # callback function to a queue
    def callback(ch, method, properties, body):
        # print(type(body), type(body.decode()))
        sleep_for = json.loads(body.decode())['sleep']
        time.sleep(sleep_for)
        print("SLEPT FOR, ", sleep_for)
        print(f"[x] Received {body.decode()}")
        
        # send a proper acknowledgement from the worker, once
        # we're done with a task, so even if it dies while working
        # this task(unacknowledged msg) is gonna be redelivered
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    
    # tell RabbitMQ to use the above function to receive messages from
# our queue, ---QUEUE must exist though---
    channel.basic_consume(
        queue='task_queue',
        on_message_callback=callback
    )

    print(' [*] Waiting for messages. To exit press CTRL + C')
    channel.start_consuming()

print(__name__, "is the caller")

if __name__ == "__main__":
    print("RUNNING CONSUMER....")
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
