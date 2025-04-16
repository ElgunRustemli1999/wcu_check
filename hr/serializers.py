from rest_framework import serializers
from .models import HRReport

class HRReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = HRReport
        fields = '__all__'
