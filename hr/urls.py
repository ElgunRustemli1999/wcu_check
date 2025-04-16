from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.HRReportListCreateAPIView.as_view(), name='hr-report-list-create'),
    path('reports/<int:pk>/', views.HRReportDetailAPIView.as_view(), name='hr-report-detail'),
]
