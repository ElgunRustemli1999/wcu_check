FROM python:3.12-slim

# Lazımi sistem paketləri
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

# Requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Layihə faylları
COPY . .

# Port (Railway avtomatik təyin edir, sadəcə EXPOSE lazımdır)
EXPOSE 8000

# Entrypoint
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn wcu_check.wsgi:application --bind 0.0.0.0:$PORT"]
