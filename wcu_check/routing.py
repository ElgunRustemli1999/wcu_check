# wcu_check/routing.py

from django.urls import re_path
from users.consumers import FaceRecognitionConsumer  # users app-inə daxil edirik

websocket_urlpatterns = [
    re_path(r'ws/recognition/$', FaceRecognitionConsumer.as_asgi()),  # WebSocket URL
]
