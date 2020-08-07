FROM python:3.7-slim-buster

RUN apt-get update -y \
    && apt-get install -y gcc libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# change the TLS version, from 1.2 to 1.0
RUN sed -i 's/TLSv1.2/TLSv1.0/g' /etc/ssl/openssl.cnf

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD [ "python3", "manage.py", "run" ]