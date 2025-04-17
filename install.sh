#!/usr/bin/env bash

echo "===== Sistemi Güncəlləyirik və Lazım olan Paketləri Quraşdırırıq ====="
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-python-dev \
    python3-dev

echo "===== pip Güncəllənir ====="
pip install --upgrade pip

echo "===== dlib ayrıca qurulur ====="
pip install dlib

echo "===== Python dependensiyalar requirements.txt ilə qurulur ====="
pip install -r requirements.txt

echo "===== GUNICORN ilə tətbiq işə salınır ====="
gunicorn wcu_check.wsgi:application
