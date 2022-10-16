import os 
import sys
from dotenv import load_dotenv

load_dotenv()

from pika import BlockingConnection, ConnectionParameters

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT= os.getenv("RABBIT_PORT", "5671")
RABBIT_USERNAME= os.getenv("RABBIT_USERNAME", "guest")
RABBIT_PASSWORD= os.getenv("RABBIT_PASSWORD", "guest")


def main():
    connection = BlockingConnection(ConnectionParameters(
                    host='rabbit-1', port=RABBIT_PORT,
                    # credentials=(RABBIT_USERNAME, RABBIT_PASSWORD)
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
        auto_ack=True,
        on_message_callback=callback
    )

    print(' [*] Waiting for messages. To exit press CTRL + C')
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
