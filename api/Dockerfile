FROM python:3.10-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

CMD ["sh", "-c", "alembic upgrade head && sh run_script.sh seed_db &&uvicorn app.main:app --host 0.0.0.0 --port 8080"]
