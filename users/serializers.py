from rest_framework import serializers
from .models import CustomUser, Worker
from core.models import Position, Department

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'is_hr', 'is_manager', 'is_employee', 'contract_start_date', 'contract_end_date']

class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    position = PositionSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Worker
        fields = ['id', 'user', 'working_type', 'position', 'department', 'face_image', 'face_encoding', 'is_active']



















"""
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        #fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'is_hr', 'is_manager', 'is_employee', 'contract_start_date', 'contract_end_date']


class WorkerSerializer(serializers.ModelSerializer):
    user = CustomUser
    class Meta:
        model = Worker
        fields = '__all__'
        # fields = ['user', 'position', 'department', 'face_image', 'face_encoding', 'is_active']
    """