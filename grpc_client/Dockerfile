FROM debian:stretch as builder
RUN apt update \
    && apt -y install curl tar

WORKDIR /tmp
RUN curl -L -o gobgp.tar.gz https://github.com/osrg/gobgp/archive/v2.0.0.tar.gz \
    && tar zxvf gobgp.tar.gz

FROM python:3.6-slim-stretch
RUN mkdir /root/proto /root/src
COPY --from=builder /tmp/gobgp-2.0.0/api/*.proto /root/proto/
COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt  --no-cache-dir
WORKDIR /root/src