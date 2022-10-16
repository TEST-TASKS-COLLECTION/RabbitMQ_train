import os 
from dotenv import load_dotenv

load_dotenv()

from pika import BlockingConnection, ConnectionParameters


RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT= os.getenv("RABBIT_PORT", "5671")
RABBIT_USERNAME= os.getenv("RABBIT_USERNAME", "guest")
RABBIT_PASSWORD= os.getenv("RABBIT_PASSWORD", "guest")

connection = BlockingConnection(ConnectionParameters(
                host='rabbit-1', port=RABBIT_PORT,
                # credentials=(RABBIT_USERNAME, RABBIT_PASSWORD)
                ))

channel = connection.channel()
channel.queue_declare(queue='hello')
