FROM python:3.12.4

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

CMD ["uvicorn","main:app"]