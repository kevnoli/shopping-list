#
FROM python:3.10

#
WORKDIR /code

#
ENV DB_HOST postgres-db

#
ENV REDIS_HOST redis-server

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY . .

#
CMD uvicorn main:app --proxy-headers --root-path /api --host 0.0.0.0 --port 8000 --reload