FROM python:3.10-slim

WORKDIR /app
COPY ./app /app
## Set the same time as the host
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata

RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -e audio-preprocess
RUN pip install -r requirements.txt