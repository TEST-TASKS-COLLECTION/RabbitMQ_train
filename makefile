rabbit_nw:
	docker network create rabbits

run_rabbit:
	docker run -d --rm --net rabbits -p 8080:15672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8

build_pub:
	docker build -t publisher applications/publisher

publisher:
	docker run -it -v ${PWD}/applications/publisher:/src/  --net rabbits --rm publisher sh

build_con:
	docker build -t consumer applications/consumer

consumer:
	docker run -it -v ${PWD}/applications/consumer:/src/  --net rabbits --rm consumer sh