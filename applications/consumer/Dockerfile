FROM python:3.9.6-alpine3.13 as build

WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY consumer.py .


FROM build as dev
ENV FLASK_APP=publisher.py
ENV FLASK_DEBUG=1
EXPOSE 8001
# CMD flask run -h 0.0.0 -p 5000
