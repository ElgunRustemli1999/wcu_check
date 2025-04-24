FROM python:3.12-slim

# Sistem paketlərini quraşdır
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    libjpeg-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements faylı
COPY requirements.txt .

# Pip upgrade və requirements-ləri qur
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



# Layihə fayllarını kopyala
COPY . .

# entrypoint scriptini əlavə et və icazə ver
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
