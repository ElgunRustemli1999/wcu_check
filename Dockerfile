FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential cmake libpq-dev git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Install dependencies including face_recognition_models
RUN pip install --upgrade pip \
    && pip install git+https://github.com/ageitgey/face_recognition_models \
    && pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
