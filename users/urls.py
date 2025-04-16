# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, WorkerViewSet, FaceStreamView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'workers', WorkerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # API endpoint-ləri
    path('worker/<int:pk>/', CustomUserViewSet.as_view({'get': 'get_worker'}), name='get_worker'),
    path('camera/', FaceStreamView.as_view(), name='camera_stream'),
]
