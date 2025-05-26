# attendance/serializers.py

from rest_framework import serializers
from .models import Attendance
from users.models import Worker


class AttendanceSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    position = serializers.CharField(source='worker.position.position_name', read_only=True)

    def get_worker(self, obj):
        return f"{obj.worker.worker_name} {obj.worker.worker_surname}"

    class Meta:
        model = Attendance
        fields = ['worker', 'position', 'date', 'check_in_time', 'check_out_time', 'late_minutes']


