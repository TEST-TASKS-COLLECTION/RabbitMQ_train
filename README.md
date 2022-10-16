# Learning RabbitMQ: NAMED QUEUE

## Create a Network

- `docker network create rabbits` so that every instance that we run can talk to eachother

## Run the Container

- `docker run -d --rm --net rabbits --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8`
  - `-d` run in detach mode
  - `--rm` remove the container once the work is done to save disk space
  - `--net rabbits` run on this network
  - `--hostname` hostname of the container
    - rabbitmq uses an `<identifier>@<hostname>` in order to talk to each other
    - if we are running rabbitmq on something like azure, vms or ec2 instances we need to make sure that we know the hostname of those instances so that these rabbitmq instances can find eachother
    - while running it on k8s its important to run it as a stateful set and not a deployment because deployment pods have random hostname
  - `--name` name of the container

### After the container is running

- `4369/tcp, 5671-5672/tcp, 15691-15692/tcp, 25672/tcp   rabbit-1`
  - if we're running in the cluster  we'll use this `4369`
  - `5671-5672`  is the communication port and for application to consume the queue
- `docker logs rabbit-1` to see that the container is up and running, and is healthy

## Inside the container

- `docker exec -it rabbit-1 bash`
- `rabbitmqctl` is cli tool that we can choose manage rabbitmq
- `rabbitmq-plugins` a separate cli, we can enable, disable, list different types of plugin integrations for rabbitmq
  - some useful plugins are:
    1. management interface plugin
    2. prometheus monitoring plugin
  - `rabbitmq-plugins list` shows that we have different plugins but most of them aren't enabled by default

## Management Plugin UI port

- `docker rm -f rabbit-1`
- `docker run -d --rm --net rabbits -p 8080:15672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8`
  - `15672` is the management plugin UI port that we can use to browse to the management instance over the browser
  - `docker exec -it rabbit-1 bash`
  - `rabbitmq-plugins enable rabbitmq_management` enables bunch of plugins
- goto browser on `localhost:8080`
  - login with default credentials **guest** and **guest**

### Channels

- Channels are virtual connections to a specific queue and this is important because when we write a program we'll be creating a connection to our rabbitmq instance and then we're going to be creating a channel which is virtual connection directly to a queue. So, we have to define a queue and then we can start putting messages into that queue

## Producer

- application that pushes messages into the queue

## Consumer

- receiving message from queue is kinda complex.
- we'll need a callback function to a queue

## Running the code

- make the consumer wait
- then make the publisher send

## Useful Commands

- `rabbitmqctl list_queues` inside the container to see how many messages are in the queues along with their name
