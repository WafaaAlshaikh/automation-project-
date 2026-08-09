import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from employees.models import Employee, LeaveRequest
from datetime import date, timedelta

user1 = User.objects.create_user(username='ahmed', password='password123', first_name='Ahmed', last_name='Hassan')
user2 = User.objects.create_user(username='sara', password='password123', first_name='Sara', last_name='Ali')

emp1 = Employee.objects.create(user=user1, department='Engineering', position='Software Engineer', hire_date=date(2023, 1, 15))
emp2 = Employee.objects.create(user=user2, department='HR', position='HR Manager', hire_date=date(2022, 6, 1))

LeaveRequest.objects.create(
    employee=emp1,
    leave_type='ANNUAL',
    start_date=date.today(),
    end_date=date.today() + timedelta(days=3),
    reason='Family vacation',
    status='PENDING'
)

LeaveRequest.objects.create(
    employee=emp1,
    leave_type='SICK',
    start_date=date.today() + timedelta(days=10),
    end_date=date.today() + timedelta(days=11),
    reason='Doctor appointment',
    status='APPROVED'
)

LeaveRequest.objects.create(
    employee=emp2,
    leave_type='EMERGENCY',
    start_date=date.today() + timedelta(days=5),
    end_date=date.today() + timedelta(days=5),
    reason='Family emergency',
    status='PENDING'
)

print("✅ Test data created successfully!")