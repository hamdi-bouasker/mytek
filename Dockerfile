FROM python:3.9.7-slim-buster
ENV PYTHONUNBUFFERED 1  
RUN pip install --upgrade pip
WORKDIR /project
COPY requirements.txt /project/
RUN pip install -r requirements.txt
