FROM brazildatacube/base:0.1

# ADD . /app

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

# CMD [ "python3", "manage.py", "run" ]