FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y \
    software-properties-common \
    nginx \
    curl \
    parallel

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.6 \
    python3.6-dev \
    python3-pip \
    python3-setuptools

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python

WORKDIR /heroku-load-balancer
COPY . /heroku-load-balancer

ENV PYTHONPATH="$PYTHONPATH:/heroku-load-balancer/src"

RUN pip3 install -r /heroku-load-balancer/requirements.txt -r /heroku-load-balancer/requirements-dev.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
