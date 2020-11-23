FROM python:3.8.5-slim-buster

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y gcc libmariadb-dev && \
    rm -rf /var/lib/apt/lists/* && \
    # change the TLS version, from 1.2 to 1.0
    sed -i 's/TLSv1.2/TLSv1.0/g' /etc/ssl/openssl.cnf

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5001

CMD [ "python", "manage.py", "run" ]
