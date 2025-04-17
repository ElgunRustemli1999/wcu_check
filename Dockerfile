# 1. Yüngül Python bazalı image istifadə olunur
FROM python:3.13-slim

# 2. Lazım olan OS paketləri (dlib və opencv üçün vacibdir)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libboost-all-dev \
    ffmpeg \
    && apt-get clean

# 3. Konteynerdə app üçün iş qovluğu yaradılır
WORKDIR /app

# 4. requirements.txt kopyalanır və pip ilə qurulur
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Layihə faylları konteynerə kopyalanır
COPY . .

# 6. Statik faylları toplayırıq
RUN python manage.py collectstatic --noinput

# 7. Port təyin olunur
EXPOSE 8000

# 8. Gunicorn ilə server start olunur
CMD ["gunicorn", "wcu_check.wsgi:application", "--bind", "0.0.0.0:8000"]
