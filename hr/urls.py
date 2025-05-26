from django.urls import path
from .views import HRReportListCreateAPIView, HRReportDetailAPIView, HRDashboardAPIView
from .views import gelenler_siyahisi,gelmeyenler_siyahisi,icazeli_siyahisi,icazesiz_siyahisi,butun_isciler_view

urlpatterns = [
    path('reports/', HRReportListCreateAPIView.as_view(), name='hr-report-list'),
    path('reports/<int:pk>/', HRReportDetailAPIView.as_view(), name='hr-report-detail'),
    path('dashboard/', HRDashboardAPIView.as_view(), name='hr-dashboard'),
    path('gelenler/', gelenler_siyahisi, name='gelenler_siyahisi'),
    path('gelmeyenler/', gelmeyenler_siyahisi, name='gelmeyenler'),
    path('icazeli/', icazeli_siyahisi, name='icazeli'),
    path('icazesiz/', icazesiz_siyahisi, name='icazesiz'),
    path('butun-isciler/',butun_isciler_view, name='butun_isciler'),
]
