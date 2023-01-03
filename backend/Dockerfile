FROM python:3.10
WORKDIR /code
ENV REDIS_HOST redis-server
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
RUN chmod +x wait-for-it.sh
ARG POSTGRES_HOST
ARG POSTGRES_PASSWORD
CMD ./wait-for-it.sh postgres-db:5432 -s -- alembic upgrade head \
    && uvicorn main:app --proxy-headers --root-path /api --host 0.0.0.0 --port 8000 --reload