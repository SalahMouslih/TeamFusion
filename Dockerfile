FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update -y && apt-get install -y default-jdk   

RUN pip install --upgrade pip

RUN pip install -r /code/requirements.txt

COPY . /code

CMD ["uvicorn", "app.core.main:app", "--reload" ,"--host", "0.0.0.0"]
