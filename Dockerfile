FROM python:3.9.5

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver"]