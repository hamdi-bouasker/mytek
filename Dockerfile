FROM python:3.9.7-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
RUN pip install --upgrade pip
WORKDIR /project
COPY requirements.txt /project/
RUN pip install -r requirements.txt
COPY . /project/
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]