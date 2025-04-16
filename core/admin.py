# core/admin.py

from django.contrib import admin
from .models import Department, Position, Holiday

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'department_name')
    search_fields = ('department_name',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position_name')
    search_fields = ('position_name',)

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date')
    search_fields = ('name', 'date')
