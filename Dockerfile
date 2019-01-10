FROM python:3.6-alpine
ADD requirements.txt /
RUN pip install -r /requirements.txt

ADD . /srv
WORKDIR /srv

CMD python report.py
