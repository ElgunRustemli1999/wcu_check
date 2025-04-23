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

# Railway PORT dəyişəni runtime-da verilir — build zamanı istifadə etmə
EXPOSE 8000

# Migrate və collectstatic build zamanı etmə — runtime-da et
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn wcu_check.wsgi:application --bind 0.0.0.0:8000"


