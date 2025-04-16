# attendance/admin.py

from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'worker', 'check_in_time', 'check_out_time', 'is_checked_in', 'extra_hours', 
        'late_minutes', 'is_holiday', 'early_leave', 'is_approved_leave', 'is_absent'
    )
    list_filter = ('is_holiday', 'is_checked_in', 'is_approved_leave')
    search_fields = [
        "worker__worker_name",
        "worker__worker_surname",
        "worker__email",
    ]

    
    # Editable field in the list display
    list_editable = ('is_approved_leave','check_in_time', 'check_out_time')  # Bu sahəni admin panelində düzəltmək olar

admin.site.register(Attendance, AttendanceAdmin)
