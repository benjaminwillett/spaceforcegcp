FROM tiangolo/meinheld-gunicorn-flask:python2.7

MAINTAINER Ben Willett "benw@techcamp.com.au"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

###update to see if github updates
