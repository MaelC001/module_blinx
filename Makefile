NAME=docker-micropython-esp8266
docker_name=blinxcb

all : docker build move

move: docker build
	docker cp "$(NAME):micropython/ports/esp8266/build-GENERIC/firmware-combined.bin" ./esp8266_micropython_build.bin

build: docker
	docker run -it -d --name $(NAME) $(docker_name)/$(NAME):latest bash \
	&& docker exec -it $(NAME) bash /create_bin.sh

docker:
	docker pull $(docker_name)/$(NAME):latest

create_image_dockerhub:
	$(eval docker=./docker-micropython)
	$(eval number_of_files=$(shell ls -A $(docker) | wc -l))
	@if [ ! -d "$(docker)" -o "$(number_of_files)" = "0" ]; then \
		git clone https://github.com/MaelC001/docker-micropython.git;\

	else \
		echo "le repertoire $(docker) n'est pas vide"; \
	fi
	cd docker-micropython &&\
	docker build -t $(NAME) . &&\
	docker run -it --name $(NAME) $(NAME) &&\
	docker tag $(NAME)  $(docker_name)/$(NAME):latest &&\
	docker commit $(NAME) $(docker_name)/$(NAME):latest &&
	docker push $(NAME) $(docker_name)/$(NAME):latest

create_mpy-cross:
	cd mpy-cross && \
	make



