from rest_framework import serializers
from .models import HRReport

class HRReportSerializer(serializers.ModelSerializer):
    worker = serializers.SerializerMethodField()
    position = serializers.CharField(source='worker.position.position_name', read_only=True)
    date = serializers.DateField(format="%Y-%m-%d")  # BURADA DÜZGÜN FORMAT

    def get_worker(self, obj):
        return f"{obj.worker.worker_name} {obj.worker.worker_surname}"

    class Meta:
        model = HRReport
        fields = ['worker', 'position', 'date', 'status']
