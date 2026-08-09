from rest_framework import serializers
from .models import Employee, LeaveRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user', 'department', 'position', 'hire_date', 'phone_number']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    days_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'employee_details', 'leave_type', 'start_date', 
                 'end_date', 'reason', 'status', 'created_at', 'updated_at', 
                 'approved_by', 'approval_date', 'days_count']
        read_only_fields = ['status', 'created_at', 'updated_at', 'approved_by', 'approval_date']