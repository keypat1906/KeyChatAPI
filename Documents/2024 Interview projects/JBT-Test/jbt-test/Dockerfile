FROM python:3.9.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -v -r requirements.txt
COPY . /usr/src/app

# This is required for the Flask cli
#ENV FLASK_APP=src/app.py

CMD flask --app src/app run
