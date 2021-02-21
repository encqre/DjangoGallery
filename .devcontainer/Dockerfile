FROM python:3.9-alpine3.12

ENV PYTHONUNBUFFERED=1

RUN apk add \
    zlib-dev \
    jpeg-dev \
    build-base \
    git

WORKDIR /workspace
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
