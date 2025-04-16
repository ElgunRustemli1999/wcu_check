# attendance/serializers.py

from rest_framework import serializers
from .models import Attendance
from users.models import Worker

class AttendanceSerializer(serializers.ModelSerializer):
    worker = serializers.StringRelatedField()  # Worker'ı ad və soyadla göstərəcək

    class Meta:
        model = Attendance
        fields = '__all__'  # Bütün sahələri serialize et
