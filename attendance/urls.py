from django.urls import path
from .views import (
    AttendanceListCreateAPIView,
    AttendanceDetailAPIView,
    AttendanceStatsAPIView,
    AllWorkersAPIView,
    attendance_hours
)

urlpatterns = [
    path('', AttendanceListCreateAPIView.as_view(), name='attendance-list-create'),
    path('<int:pk>/', AttendanceDetailAPIView.as_view(), name='attendance-detail'),
    path('stats/', AttendanceStatsAPIView.as_view(), name='attendance-stats'),
    path('workers/all/', AllWorkersAPIView.as_view(), name='all-workers'),
    path('hours/', attendance_hours, name='attendance_hours'),
]
