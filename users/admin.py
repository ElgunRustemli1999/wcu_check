from django.contrib import admin
from .models import CustomUser, Worker
from django.contrib.auth.admin import UserAdmin
from django import forms

from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"





# CustomUser admin
class CustomUserAdmin(UserAdmin):
    form = CustomUserCreationForm

    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_hr', 'is_employee']
    list_filter = ['is_staff', 'is_superuser', 'is_hr', 'is_employee']

    fieldsets = UserAdmin.fieldsets + (
        ("Əlavə Məlumat", {
            "fields": (
                'phone_number',
                'contract_start_date',
                'contract_end_date',
                'is_hr',
                'is_manager',
                'is_employee',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Əlavə Məlumat", {
            "fields": (
                'email',
                'phone_number',
                'contract_start_date',
                'contract_end_date',
                'is_hr',
                'is_manager',
                'is_employee',
            )
        }),
    )

    search_fields = ['email']
    ordering = ['email']



# Worker admin (user sahəsi olmadan)
class WorkerAdmin(admin.ModelAdmin):
    list_display = (
        'worker_name', 'worker_surname', 'email', 'phone_number', 
        'position', 'department', 'working_type', 'is_active', 
        'contract_start_date', 'contract_end_date'
    )
    search_fields = ['worker_name', 'worker_surname', 'email', 'position__position_name', 'department__department_name']
    list_filter = ['working_type', 'is_active', 'position', 'department']

# Qeydiyyat
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Worker, WorkerAdmin)
