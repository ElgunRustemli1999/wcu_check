from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import AllowAny

# Attendance API Views

# Attendance List and Create
class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny] 

# Attendance Detail View (Retrieve, Update, Delete)
class AttendanceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny] 

class AttendanceStatsAPIView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        data = []
        for obj in Attendance.objects.select_related("worker").all():
            data.append({
                "worker": f"{obj.worker.worker_name} {obj.worker.worker_surname}",
                "check_in": obj.check_in_time is not None,
                "late_minutes": obj.late_minutes,
            })
        return Response(data)