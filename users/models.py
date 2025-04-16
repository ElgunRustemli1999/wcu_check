from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import Department, Position
import base64
import os
import face_recognition
import numpy as np

# ====================== Custom User ==========================
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

# ====================== Worker ==========================
class Worker(models.Model):
    FULL_TIME = 'full_time'
    PART_TIME_MORNING = 'part_time_morning'
    PART_TIME_AFTERNOON = 'part_time_afternoon'
    
    WORKING_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time (9:00–18:00)'),
        (PART_TIME_MORNING, 'Part Time Morning (9:00–13:00)'),
        (PART_TIME_AFTERNOON, 'Part Time Afternoon (14:00–18:00)'),
    ]

    @classmethod
    def add_working_type(cls, type_name, description):
        """Yeni iş rejimi əlavə etmək üçün istifadə olunur"""
        cls.WORKING_TYPE_CHOICES.append((type_name, description))

    # Əsas sahələr
    worker_name = models.CharField(max_length=35)
    worker_surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)

    # İdarəedici sahələr
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    working_type = models.CharField(
        max_length=20,
        choices=WORKING_TYPE_CHOICES,
        default=FULL_TIME,
    )
    is_active = models.BooleanField(default=True)
    has_permission_to_leave_early = models.BooleanField(default=False)

    # Üz şəkli və encoding
    face_image = models.ImageField(upload_to="faces/")
    face_encoding = models.TextField(null=True, blank=True)  # Base64 string

    def __str__(self):
        return f"{self.worker_name} {self.worker_surname}"

    def save(self, *args, **kwargs):
        # Faylı burda oxuma – signals.py-də on_commit ilə et
        super().save(*args, **kwargs)

    def update_face_encoding(self):
        """Şəkildən üz encoding alınır və saxlanır"""
        if self.face_image and os.path.exists(self.face_image.path):
            try:
                image = face_recognition.load_image_file(self.face_image.path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    arr = encodings[0].astype(np.float64)  # Yoxsa bəzi sistemlərdə float32 ola bilər
                    self.face_encoding = base64.b64encode(arr.tobytes()).decode('utf-8')
                else:
                    self.face_encoding = None
            except Exception as e:
                self.face_encoding = None
