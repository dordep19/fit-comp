FROM python:3.9.5

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]