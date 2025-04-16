# users/routing.py

from django.urls import re_path
from .consumers import FaceRecognitionConsumer

websocket_urlpatterns = [
    re_path(r'ws/recognition/$', FaceRecognitionConsumer.as_asgi()),  # WebSocket URL
]
