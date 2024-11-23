FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y \
    software-properties-common \
    nginx \
    curl

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.6 \
    python3.6-dev \
    python3-pip \
    python3-setuptools

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python

WORKDIR /heroku-load-balancer
COPY . /heroku-load-balancer

ENV PYTHONPATH="$PYTHONPATH:/heroku-load-balancer/src"

RUN pip3 install -r /heroku-load-balancer/requirements.txt -r /heroku-load-balancer/requirements-dev.txt gunicorn

EXPOSE 8000

CMD /bin/bash -c "python3 src/entrypoint.py create-load-balancer --nginx-port=$PORT --heroku-api-key=$HEROKU_API_KEY --pipeline-identifier=$PIPELINE_IDENTIFIER" && mv nginx.conf /etc/nginx/nginx.conf && nginx && gunicorn -w 3 -b 0.0.0.0:$PORT src.entrypoint:create_load_balancer_app
