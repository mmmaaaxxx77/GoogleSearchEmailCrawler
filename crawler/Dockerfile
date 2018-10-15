FROM python:3.6.3
ENV PYTHONBUFFERED 1
RUN mkdir /app
RUN mkdir /tmp/excel
WORKDIR /app
ADD . /app
RUN pip install -r pip.txt
#RUN python manage.py runserver
