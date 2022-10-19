# Learning RabbitMQ: Publish/Subscribe- SIMPLE DOCKER-COMPOSE

[RabbitMQ docs](https://www.rabbitmq.com/tutorials/tutorial-three-python.html)

## To Run

- `docker-compose up`

## Useful Commands

- `rabbitmqctl list_queues` inside the container to see how many messages are in the queues along with their name
- `rabbitmqctl list_queues name messages_ready messages_unacknowledged` to see the name, ready message and the messages that are unacknowledged
  - very useful when we have forgotten to put basic acknowledgement in our code which will result in more and more memory consumption
