FROM python:3.12

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

ADD .env.docker /code/.env

RUN mkdir media

EXPOSE 8000

RUN python manage.py migrate

RUN pytest ./root_app/tests/tests.py -vv

CMD python manage.py runserver