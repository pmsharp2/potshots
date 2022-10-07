FROM ubuntu:20.04

MAINTAINER pete

RUN apt-get update -y && apt-get install -y python3-pip python-dev

COPY /app/requirements.txt /app/requirements.txt

WORKDIR /app
RUN python --version
RUN pip3 install -r /app/requirements.txt
run pip3 list
COPY /app /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
