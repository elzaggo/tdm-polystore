PSWD=foobar
#IMAGE=timescale/timescaledb
IMAGE=timescale/timescaledb-postgis

images:
	docker build -f docker/Dockerfile.hdfs -t tdm/hdfs docker
	docker build -f docker/Dockerfile.tiledb -t tdm/tiledb docker
	rm -rf docker/tdmq-dist ; mkdir docker/tdmq-dist
	cp -a setup.py tdmq docker/tdmq-dist
	cp -a tests/data tdmq docker/tdmq-dist
	docker build -f docker/Dockerfile.web -t tdm/web docker


run: images
	sed -e "s^LOCAL_PATH^$${PWD}^" -e "s^USER_UID^$$(id -u)^" \
            -e "s^USER_GID^$$(id -g)^"  \
            < docker/docker-compose.yml-tmpl > docker/docker-compose.yml
	docker-compose -f ./docker/docker-compose.yml up

clean:
	docker-compose -f ./docker/docker-compose.yml down

