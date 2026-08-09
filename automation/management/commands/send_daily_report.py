from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .scripts import generate_daily_report, auto_approve_emergency_requests
from .ai_integration import summarize_pending_requests
from automation.ai_integration import summarize_leave_requests_with_ai

@shared_task
def send_daily_report_email_task():
    report = generate_daily_report()
    
    # send_mail(
    #     subject=f'Daily Leave Report - {timezone.now().date()}',
    #     message=report,
    #     from_email='noreply@company.com',
    #     recipient_list=['manager@company.com'],
    # )
    
    return f"Report sent: {len(report)} characters"

@shared_task
def auto_approve_emergency_task():
    count = auto_approve_emergency_requests()
    return f"Auto-approved {count} emergency requests"

@shared_task
def generate_ai_summary_task():
    summary = summarize_pending_requests()
    return summary