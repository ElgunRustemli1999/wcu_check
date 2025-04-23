FROM python:3.12-slim

# Sistem paketləri quraşdırılır
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

# İş qovluğu
WORKDIR /app

# Asılılıqlar
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Layihə faylları
COPY . .

# Django migration + collectstatic + gunicorn server
CMD bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn wcu_check.wsgi:application --bind 0.0.0.0:8000"
