FROM python:3.7-slim-buster

RUN apt-get update -y \
    && apt-get install -y gcc libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "manage.py", "run" ]