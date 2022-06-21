FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh && \
    bash /tmp/nodesource_setup.sh && \
    apt-get install -y nodejs

COPY . /app

WORKDIR /app/src/authsign/client

RUN npm install && \
    npm run build

WORKDIR /app

RUN pip3 install -r requirements.txt

RUN flask db upgrade

RUN flask run --port=8088