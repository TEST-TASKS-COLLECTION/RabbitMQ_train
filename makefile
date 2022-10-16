build_pub:
	docker build -t publisher applications/publisher

publisher:
	docker run -it -v ${PWD}/applications/publisher:/src/  --net rabbits --rm publisher sh

build_con:
	docker build -t consumer applications/consumer

consumer:
	docker run -it -v ${PWD}/applications/consumer:/src/  --net rabbits --rm consumer sh