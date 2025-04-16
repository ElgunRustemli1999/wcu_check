# core/urls.py

from django.urls import path
from .views import DepartmentListCreateAPIView, DepartmentDetailAPIView, PositionListCreateAPIView, PositionDetailAPIView, HolidayListCreateAPIView, HolidayDetailAPIView

urlpatterns = [
    # Department Routes
    path('departments/', DepartmentListCreateAPIView.as_view(), name='department-list'),
    path('departments/<int:pk>/', DepartmentDetailAPIView.as_view(), name='department-detail'),

    # Position Routes
    path('positions/', PositionListCreateAPIView.as_view(), name='position-list'),
    path('positions/<int:pk>/', PositionDetailAPIView.as_view(), name='position-detail'),

    # Holiday Routes
    path('holidays/', HolidayListCreateAPIView.as_view(), name='holiday-list'),
    path('holidays/<int:pk>/', HolidayDetailAPIView.as_view(), name='holiday-detail'),
]
