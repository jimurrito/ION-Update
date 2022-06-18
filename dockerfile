# Docker Container for Ion-Update

FROM jfloff/alpine-python:latest

ARG UNIT=days
ENV UNIT=${UNIT}
ARG AMOUNT=1
ENV AMOUNT=${AMOUNT}
ARG SCOPE
ENV SCOPE=${SCOPE}
ARG PUBKEY
ENV PUBKEY=${PUBKEY}
ARG PRVKEY
ENV PRVKEY=${PRVKEY}

USER root

ADD App/. /config/.

RUN apk update && apk upgrade && pip3 install --upgrade pip
RUN pip3 install requests datetime

WORKDIR /config

CMD python3 ionos-DMUP.py --unit ${UNIT} --amount ${AMOUNT} --scope ${SCOPE} --pubkey ${PUBKEY} --prvkey ${PRVKEY}
