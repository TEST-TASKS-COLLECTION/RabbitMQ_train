from json import load
from flask import Flask, request

import json

import os
from dotenv import load_dotenv

load_dotenv()

from pika import BlockingConnection, ConnectionParameters, \
                 BasicProperties
from pika.spec import PERSISTENT_DELIVERY_MODE


RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
RABBIT_PORT= int(os.getenv("RABBIT_PORT", "5671"))
RABBIT_USERNAME= os.getenv("RABBIT_USERNAME", "guest")
RABBIT_PASSWORD= os.getenv("RABBIT_PASSWORD", "guest")

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>HELLO WORLD!</h1>"

def set_connection(data):
    print("*"*20)
    print("connecting to host", RABBIT_HOST, RABBIT_PORT, "set publisher")
    print("*"*20)
    connection = BlockingConnection(ConnectionParameters(
                host=RABBIT_HOST, port=RABBIT_PORT,  # type: ignore
                # credentials=(RABBIT_USERNAME, RABBIT_PASSWORD)
                ))
    channel = connection.channel()
    
    # create a hello queue to which the message will be delivered
    channel.queue_declare(queue="task_queue", durable=True)
    
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(data),
        properties=BasicProperties(
            delivery_mode = PERSISTENT_DELIVERY_MODE
        )
    )
    
    connection.close()

@app.route("/publish", methods=["POST",])
def publish():
    print("IN PUBLISH")
    channel = set_connection(data=request.json)
    # try:
    #     res = request.json
    # except:
    #     res = request.data
    
    return "Message Passed", 200


