from celery import shared_task
from django.utils import timezone
from employees.models import LeaveRequest

@shared_task
def send_daily_report():
    pending = LeaveRequest.objects.filter(status='PENDING')
    report = f"📊 Daily Report - {timezone.now().date()}\n"
    report += f"Pending requests: {pending.count()}\n"
    for req in pending:
        report += f"- {req.employee.user.first_name}: {req.get_leave_type_display()}\n"
    print(report)
    return report

@shared_task
def auto_approve_emergency():
    emergency = LeaveRequest.objects.filter(status='PENDING', leave_type='EMERGENCY')
    count = 0
    for req in emergency:
        if req.days_count <= 2:
            req.status = 'APPROVED'
            req.approval_date = timezone.now()
            req.save()
            count += 1
    return f"Auto-approved {count} emergency requests"