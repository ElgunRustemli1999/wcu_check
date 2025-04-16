from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser, Worker
from .serializers import CustomUserSerializer, WorkerSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.generic import TemplateView

# CustomUser viewset
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_worker(self, request, pk=None):
        user = self.get_object()
        try:
            worker = Worker.objects.get(user=user)
            worker_serializer = WorkerSerializer(worker)
            return Response(worker_serializer.data)
        except Worker.DoesNotExist:
            return JsonResponse({"error": "Worker not found for this user."}, status=404)

# Worker viewset
class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_user(self, request, pk=None):
        worker = self.get_object()
        user = worker.user
        user_serializer = CustomUserSerializer(user)
        return Response(user_serializer.data)
# Bu sadəcə HTML səhifəni göstərmək üçündür
class FaceStreamView(TemplateView):
    template_name = 'face_stream.html'
