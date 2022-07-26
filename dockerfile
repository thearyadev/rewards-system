FROM python:3.10.2-slim-buster

WORKDIR /rewards-system

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN apt-get update
RUN apt-get install nano
RUN apt-get install -y iputils-ping
RUN apt-get install -y net-tools
ENV TZ=America/Toronto

CMD ["python3", "./app.py"]