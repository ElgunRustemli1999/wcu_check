FROM python:3.12

# Sistemdə lazım olan kitabxanalar
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
RUN pip install git+https://github.com/ageitgey/face_recognition_models.git
# Requirements və əlavə paket
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
# face_recognition_models ayrıca çağırılır


# Layihə faylları və entrypoint
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
