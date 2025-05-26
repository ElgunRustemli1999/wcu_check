from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Attendance
from .serializers import AttendanceSerializer
from users.models import Worker
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
# ✅ Attendance List and Create (CRUD List & Create)
class AttendanceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]


# ✅ Attendance Detail View (CRUD Retrieve, Update, Delete)
class AttendanceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]


# ✅ Attendance Statistics View (Gələn və Gəlməyən İşçilər)
class AttendanceStatsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = []
        today = timezone.now().date()
        all_workers = Worker.objects.filter(is_active=True)

        # Bu gün gələn işçiləri al
        attended_workers = Attendance.objects.select_related("worker").filter(check_in_time__date=today)
        attended_worker_ids = set(att.worker.id for att in attended_workers)

        for worker in all_workers:
            has_attended = worker.id in attended_worker_ids
            attendance_record = attended_workers.filter(worker=worker).first()
            late_minutes = attendance_record.late_minutes if attendance_record else 0

            data.append({
                "worker": f"{worker.worker_name} {worker.worker_surname}",
                "position": worker.position.position_name if worker.position else "-",
                "check_in": has_attended,
                "late_minutes": late_minutes,
            })

        return Response(data)


# ✅ All Workers View (Bütün Aktiv İşçiləri Listələyir)
class AllWorkersAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        workers = Worker.objects.filter(is_active=True)
        data = [{
            "id": w.id,
            "name": f"{w.worker_name} {w.worker_surname}",
            "position": w.position.position_name if w.position else "-"
        } for w in workers]
        return Response(data)
    
def attendance_hours(request):
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    # Tarixləri yoxlayırıq və valid olub-olmadığını test edirik
    if not start_date or not end_date:
        return JsonResponse({'error': 'Start and end date are required'}, status=400)

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    all_workers = Worker.objects.filter(is_active=True)
    attendance_records = Attendance.objects.filter(
        Q(check_in_time__date__range=(start, end)) |
        Q(check_out_time__date__range=(start, end))
    ).select_related('worker', 'worker__position')

    worker_map = {}
    for record in attendance_records:
        wid = record.worker.id
        worker_map[wid] = {
            'worker': f"{record.worker.worker_name} {record.worker.worker_surname}",
            'check_in_time': record.check_in_time.strftime('%H:%M') if record.check_in_time else None,
            'check_out_time': record.check_out_time.strftime('%H:%M') if record.check_out_time else None,
            'late_minutes': record.late_minutes or 0,
            'date': record.check_in_time.date().isoformat() if record.check_in_time else '',
            'position': record.worker.position.position_name if record.worker.position else "-"
        }

    data = []
    for worker in all_workers:
        if worker.id in worker_map:
            data.append(worker_map[worker.id])
        else:
            data.append({
                'worker': f"{worker.worker_name} {worker.worker_surname}",
                'check_in_time': None,
                'check_out_time': None,
                'late_minutes': 0,
                'date': '',
                'position': worker.position.position_name if worker.position else "-"
            })

    return JsonResponse(data, safe=False)