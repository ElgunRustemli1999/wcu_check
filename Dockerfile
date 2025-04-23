FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PORT=8000

RUN python manage.py migrate && python manage.py collectstatic --noinput

CMD ["gunicorn", "wcu_check.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
