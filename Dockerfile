FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r /code/requirements.txt

COPY ./app /code/app

COPY ./tests/ /code/tests/

ENTRYPOINT ["uvicorn", "app.core.main:app", "--reload" ,"--host", "0.0.0.0"]
