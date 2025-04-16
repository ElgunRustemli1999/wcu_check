from rest_framework import generics
from .models import HRReport
from .serializers import HRReportSerializer
from rest_framework.permissions import AllowAny

class HRReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = HRReport.objects.all()
    serializer_class = HRReportSerializer
    permission_classes = [AllowAny]

class HRReportDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HRReport.objects.all()
    serializer_class = HRReportSerializer
    permission_classes = [AllowAny]
