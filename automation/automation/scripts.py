from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from employees.models import LeaveRequest, Employee

def generate_daily_report():
    """Generate a report of pending leave requests"""
    today = timezone.now().date()
    pending_requests = LeaveRequest.objects.filter(status='PENDING')
    
    report = f"📋 Daily Leave Report - {today}\n"
    report += "=" * 50 + "\n"
    report += f"Total Pending Requests: {pending_requests.count()}\n\n"
    
    for req in pending_requests:
        report += f"- {req.employee.user.first_name} {req.employee.user.last_name}\n"
        report += f"  Type: {req.get_leave_type_display()}\n"
        report += f"  Dates: {req.start_date} to {req.end_date}\n"
        report += f"  Reason: {req.reason}\n\n"
    
    return report

def send_daily_report_email():
    """Send daily report via email (console for now)"""
    report = generate_daily_report()
    
    # For testing, we'll print to console
    print("\n" + "="*60)
    print("📧 EMAIL REPORT SENT:")
    print(report)
    print("="*60 + "\n")
    
    # In production, uncomment this:
    # send_mail(
    #     subject=f'Daily Leave Report - {timezone.now().date()}',
    #     message=report,
    #     from_email='noreply@company.com',
    #     recipient_list=['manager@company.com'],
    #     fail_silently=False,
    # )
    
    return report

def auto_approve_emergency_requests():
    """Auto-approve emergency leave requests if less than 2 days"""
    emergency_requests = LeaveRequest.objects.filter(
        status='PENDING',
        leave_type='EMERGENCY'
    )
    
    approved_count = 0
    for req in emergency_requests:
        if req.days_count <= 2:
            req.status = 'APPROVED'
            req.approval_date = timezone.now()
            req.save()
            approved_count += 1
    
    return approved_count

def process_weekly_summary():
    """Generate weekly summary of all leave requests"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    requests = LeaveRequest.objects.filter(created_at__date__gte=week_ago)
    
    summary = f"📊 Weekly Leave Summary - {today}\n"
    summary += "=" * 50 + "\n"
    summary += f"Total Requests: {requests.count()}\n"
    summary += f"Pending: {requests.filter(status='PENDING').count()}\n"
    summary += f"Approved: {requests.filter(status='APPROVED').count()}\n"
    summary += f"Rejected: {requests.filter(status='REJECTED').count()}\n"
    
    return summary