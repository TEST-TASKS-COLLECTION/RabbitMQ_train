from json import load
from flask import Flask, request

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

# create a hello queue to which the message will be delivered
channel.queue_declare(queue="hello")

channel.basic_publish(
    exchange="", # a message always go through exchange to a queue
    routing_key='hello', # queue name
    body="Hello World"
)

print("[x] SENT 'HELLO WORLD!'")


# naje sure n/w buffers were flushed and our message was delivered
# to RabbitMQ
connection.close()

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>HELLO WORLD!</h1>"

@app.route("/publish", methods=["POST",])
def publish():
    res = request.json