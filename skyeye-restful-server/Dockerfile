FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /skyeye-docker-server
ADD . /skyeye-docker-server

WORKDIR /skyeye-docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# EXPOSE 8000
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]