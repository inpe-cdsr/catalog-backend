FROM python:3.7-slim-buster

RUN apt-get update -y \
    && apt-get install -y gcc libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# CMD [ "python3", "manage.py", "run" ]