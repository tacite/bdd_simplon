FROM python:3.12.4

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]


# docker build -t monimage:latest .
# docker run --rm -d --env-file .env -p 5000:5000 -v $(pwd):/app monimage