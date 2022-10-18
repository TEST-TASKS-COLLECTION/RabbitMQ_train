# Learning RabbitMQ: WORK QUEUES- SIMPLE DOCKER-COMPOSE

## To Run

- `docker-compose up`

## Work Queue

- Work Queue will be used to distribute time-consuming tasks among multiple workers.
- The main idea behind Work Queues (aka: Task Queues) is to avoid doing a resource-intensive task immediately and having to wait for it to complete. Instead we shedule the task to be done later
- We encapsulate a task as a message and send it to the queue.
- A worker process running in the background will pop the tasks (from queue) and eventually execute the job. When you run many workers the tasks will be shared between them.

- $\color{green}This \space concept \space is \space especially \space useful \space in \space web \space applications \space where \space it's \space impossible \space to \space handle \space a \space complex \space task \space during \space a \space short \space HTTP \space request \space window.$

- [more at](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)

## Round-robin dispatching

- If we have more than one workers, by default on average every consumer will get the same number of messages. This way of distributing messages is called round-robin

## Message Acknowledgement

- Previously, if our worker dies we'd lose any tasks but that's not what we want. What was happening there is that once RabbitMQ delivers message to the consumer it immediately marks it for deletion.
- So in order to make sure a message is never lost, RabbitMQ supports message acknowledgements. An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been received, processed and that RabbitMQ is free to delete it.
- If a consumer dies(its channel is closed, connection is closed, or TCP connection is lost) without sending an ack, RabbitMQ will understand that a message wasn't processed fully and will re-queue it
- If there are other consumers online at the same time, it will then quickly redeliver it to another consumer.
- That way you can be sure that no message is lost, even if the workers occasionally die.
- inside of callback function `ch.basic_ack(delivery_tag = method.delivery_tag)`

## Durable

- even if the RabbitMQ server stops we don't want to lose our tasks
- `channel.queue_declare(queue='task_queue', durable=True)`
  - RabbitMQ doesn't allow you to redefine an existing queue with different parameters and will return an error to any program that tries to do that. And that's why I didn't use `hello` there

### Message Persistence

- we can mark our messages as persistent by `properties=pika.BasicProperties(delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE))` when doing our publishing
- this doesn't fully guarantee that a msg won't be lost. Although it'll tell RabbitMQ to save the msg to a disk, *there's still a short time window when RabbitMQ has accepted a message and hasn't saved it yet*
- Also, RabbitMQ doesn't do fsync(2) for every message -- it may be just saved to cache and not really written to the disk

## Fair Dispatch

- RabbitMQ just dispatches a message when the message enters the queue. It doesn't look at the number of unacknowledged messages for a consumer. So a worker might be constantly busy and the other one does hardly any work.
- To make sure that the messages are equally divided i.e message gets dispatched to a free worker when another is busy.
- `channel.basic_qos(prefetch_count=1)` don't dispatch a new message to a worker until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy
- If all the workers are busy then the queue can fill up. We will want to keep an eye on that, and maybe add more workers, or use [message TTL](https://www.rabbitmq.com/ttl.html)

## Useful Commands

- `rabbitmqctl list_queues` inside the container to see how many messages are in the queues along with their name
- `rabbitmqctl list_queues name messages_ready messages_unacknowledged` to see the name, ready message and the messages that are unacknowledged
  - very useful when we have forgotten to put basic acknowledgement in our code which will result in more and more memory consumption
