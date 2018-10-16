FROM python:3.6.3
ENV PYTHONBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD . /app
RUN pip install -r pip.txt
RUN mkdir /db
RUN python manage.py collectstatic --noinput
#RUN python manage.py runserver
