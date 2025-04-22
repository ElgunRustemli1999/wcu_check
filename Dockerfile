FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential cmake libpq-dev git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN chmod +x entrypoint.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
