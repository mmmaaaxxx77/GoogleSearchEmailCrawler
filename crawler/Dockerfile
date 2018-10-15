FROM python:3.6.3

RUN mkdir /app
# Install chrome driver
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

WORKDIR /app/chromeDriver
RUN apt-get install -y unzip
RUN apt-get install -y libnss3-dev
RUN wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN apt-get remove -y unzip

# Install gecko driver
WORKDIR /app/geckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.22.0/geckodriver-v0.22.0-linux64.tar.gz
RUN tar -zxvf geckodriver-v0.22.0-linux64.tar.gz

# set display port to avoid crash
ENV DISPLAY=:99

ENV PYTHONBUFFERED 1
RUN mkdir /tmp/excel
WORKDIR /app
ADD . /app
RUN pip install -r pip.txt
#RUN python manage.py runserver
