# syntax=docker/dockerfile:1

FROM python:3.10-rc-slim-buster

WORKDIR /app-contable

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

CMD [ "python", "app.py"]