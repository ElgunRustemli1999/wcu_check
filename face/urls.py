from django.urls import path
from . import views

urlpatterns = [
    path('recognize/', views.recognize_face, name='recognize_face'),
    path('video_feed/', views.video_feed, name='video_feed'),
    

]
