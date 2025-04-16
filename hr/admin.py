from django.contrib import admin
from .models import HRReport

class HRReportAdmin(admin.ModelAdmin):
    list_display = ('worker', 'status', 'date', 'comment')
    search_fields = ('worker__user__first_name', 'worker__user__last_name')

admin.site.register(HRReport, HRReportAdmin)
