FROM python:3.6.3

RUN mkdir /app
# Install chrome driver
WORKDIR /app/chromeDriver
RUN apt-get update
RUN apt-get install unzip libnss3-dev libgconf
RUN wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN apt-get remove -y unzip

# Install gecko driver
WORKDIR /app/geckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.22.0/geckodriver-v0.22.0-linux64.tar.gz
RUN tar -zxvf geckodriver-v0.22.0-linux64.tar.gz


WORKDIR /app/GoogleScraper

ENV PYTHONBUFFERED 1
RUN mkdir /tmp/excel
WORKDIR /app
ADD . /app
RUN pip install -r pip.txt
#RUN python manage.py runserver
