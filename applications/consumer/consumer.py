import os 
import sys
from dotenv import load_dotenv

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
                    host=RABBIT_HOST, port=RABBIT_PORT,
                    ))

    channel = connection.channel()
    channel.queue_declare(queue='hello')
    
    # callback function to a queue
    def callback(ch, method, properties, body):
        print(f"[x] Received {body.decode()}")
    
    # tell RabbitMQ to use the above function to receive messages from
# our queue, ---QUEUE must exist though---
    channel.basic_consume(
        queue='hello',
        auto_ack=False,
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
