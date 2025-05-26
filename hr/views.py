from rest_framework import generics
from .models import HRReport
from .serializers import HRReportSerializer
from rest_framework.permissions import AllowAny
from users.models import Worker
from django.db.models import Q
from attendance.models import Attendance
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render
from users.models import Worker
from hr.models import HRReport
from django.core.paginator import Paginator
from datetime import datetime, timedelta

class HRReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = HRReport.objects.all()
    serializer_class = HRReportSerializer
    permission_classes = [AllowAny]

class HRReportDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HRReport.objects.all()
    serializer_class = HRReportSerializer
    permission_classes = [AllowAny]

class HRDashboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        start_date = request.GET.get('start', timezone.now().date())
        end_date = request.GET.get('end', timezone.now().date())

        all_workers = Worker.objects.filter(is_active=True)
        hr_reports = HRReport.objects.filter(date__range=[start_date, end_date])
        attendance_records = Attendance.objects.filter(
            Q(check_in_time__date__range=[start_date, end_date]) |
            Q(check_out_time__date__range=[start_date, end_date])
        )

        present_worker_ids = set(attendance_records.values_list('worker_id', flat=True))
        hr_map = {report.worker.id: report.statioun for report in hr_reports}

        data = []
        for worker in all_workers:
            status = "icazəsiz"
            if worker.id in present_worker_ids:
                status = "gəlib"
            elif worker.id in hr_map:
                status = hr_map[worker.id]  # icazəli və ya digər statuslar

            data.append({
                'id': worker.id,
                'worker': f"{worker.worker_name} {worker.worker_surname}",
                'position': worker.position.position_name if worker.position else "-",
                'status': status,
                'date': str(start_date)
            })

        return Response(data)

def gelenler_siyahisi(request):
    range_type = request.GET.get("range", "day")
    start = request.GET.get("start")
    end = request.GET.get("end")

    today = datetime.today().date()
    
    if range_type == "week":
        start_date = today - timedelta(days=6)
        end_date = today
    elif range_type == "month":
        start_date = today - timedelta(days=29)
        end_date = today
    elif range_type == "custom" and start and end:
        start_date = datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.strptime(end, '%Y-%m-%d').date()
    else:  # default is today
        start_date = end_date = today

    queryset = Attendance.objects.filter(check_in_time__date__range=(start_date, end_date)).select_related('worker', 'worker__position', 'worker__department').order_by('-check_in_time')

    paginator = Paginator(queryset, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "range_type": range_type,
        "start_date": start_date,
        "end_date": end_date,
    }
    return render(request, 'gelenler.html', context)
def gelmeyenler_siyahisi(request):
    range_type = request.GET.get("range", "day")
    start = request.GET.get("start")
    end = request.GET.get("end")
    today = datetime.today().date()

    if range_type == "week":
        start_date = today - timedelta(days=6)
        end_date = today
    elif range_type == "month":
        start_date = today - timedelta(days=29)
        end_date = today
    elif range_type == "custom" and start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    else:
        start_date = end_date = today

    all_workers = Worker.objects.filter(is_active=True).select_related('position', 'department')
    date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    absents = []

    for date in date_list:
        # həmin gün gələnlər
        present_ids = Attendance.objects.filter(check_in_time__date=date).values_list('worker_id', flat=True)
        # həmin gün icazəlilər
        excused_ids = HRReport.objects.filter(date=date, status='icazəli').values_list('worker_id', flat=True)

        # gəlməyənlər = bütün - gələnlər - icazəlilər
        missing_workers = all_workers.exclude(id__in=present_ids).exclude(id__in=excused_ids)

        for worker in missing_workers:
            absents.append({
                "name": f"{worker.worker_name} {worker.worker_surname}",
                "position": worker.position.position_name if worker.position else "-",
                "department": worker.department.department_name if worker.department else "-",
                "date": date.strftime("%Y-%m-%d")
            })

    # pagination
    paginator = Paginator(absents, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "gelmeyenler.html", {
        "page_obj": page_obj,
        "range_type": range_type,
        "start_date": start_date,
        "end_date": end_date,
    })



def icazeli_siyahisi(request):
    range_type = request.GET.get("range", "day")
    start = request.GET.get("start")
    end = request.GET.get("end")

    today = datetime.today().date()

    if range_type == "week":
        start_date = today - timedelta(days=6)
        end_date = today
    elif range_type == "month":
        start_date = today - timedelta(days=29)
        end_date = today
    elif range_type == "custom" and start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    else:
        start_date = end_date = today

    # HRReport'dan yalnız icazəliləri çək
    reports = HRReport.objects.filter(
        status="icazəli",
        date__range=(start_date, end_date)
    ).select_related('worker', 'worker__position', 'worker__department').order_by('-date')

    paginator = Paginator(reports, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = [{
        "name": f"{r.worker.worker_name} {r.worker.worker_surname}",
        "position": r.worker.position.position_name if r.worker.position else "-",
        "department": r.worker.department.depatment_name if r.worker.department else "-",
        "date": r.date.strftime("%Y-%m-%d")
    } for r in page_obj]

    return render(request, "icazeli.html", {
        "page_obj": data,
        "range_type": range_type,
        "start_date": start_date,
        "end_date": end_date,
    })

def icazesiz_siyahisi(request):
    range_type = request.GET.get("range", "day")
    start = request.GET.get("start")
    end = request.GET.get("end")

    today = datetime.today().date()

    if range_type == "week":
        start_date = today - timedelta(days=6)
        end_date = today
    elif range_type == "month":
        start_date = today - timedelta(days=29)
        end_date = today
    elif range_type == "custom" and start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    else:
        start_date = end_date = today

    # HRReport'dan yalnız icazəsiz olanları çək
    reports = HRReport.objects.filter(
        status="icazəsiz",
        date__range=(start_date, end_date)
    ).select_related('worker', 'worker__position', 'worker__department').order_by('-date')

    paginator = Paginator(reports, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = [{
        "name": f"{r.worker.worker_name} {r.worker.worker_surname}",
        "position": r.worker.position.position_name if r.worker.position else "-",
        "department": r.worker.department.title if r.worker.department else "-",
        "date": r.date.strftime("%Y-%m-%d")
    } for r in page_obj]

    return render(request, "icazesiz.html", {
        "page_obj": data,
        "range_type": range_type,
        "start_date": start_date,
        "end_date": end_date,
    })
def butun_isciler_view(request):
    workers = Worker.objects.filter(is_active=True).select_related('position')
    return render(request, 'butun_isciler.html',{'workers':workers})
