FROM python:3.8

RUN mkdir /onceo-test-task

WORKDIR /onceo-test-task

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000