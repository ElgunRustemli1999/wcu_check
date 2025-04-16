# attendance/urls.py

from django.urls import path
from .views import AttendanceListCreateAPIView, AttendanceDetailAPIView
from .views import AttendanceStatsAPIView

urlpatterns = [
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance-list-create'),
    path('attendance/<int:pk>/', AttendanceDetailAPIView.as_view(), name='attendance-detail'),
    path('hours/', AttendanceStatsAPIView.as_view(), name='attendance-hours'),
]
