from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .scripts import generate_daily_report, auto_approve_emergency_requests
from .ai_integration import summarize_pending_requests

@shared_task
def send_daily_report_email_task():
    """إرسال التقرير اليومي عبر البريد الإلكتروني (مهمة خلفية)"""
    report = generate_daily_report()
    
    # إرسال البريد (في الإنتاج)
    # send_mail(
    #     subject=f'Daily Leave Report - {timezone.now().date()}',
    #     message=report,
    #     from_email='noreply@company.com',
    #     recipient_list=['manager@company.com'],
    # )
    
    return f"Report sent: {len(report)} characters"

@shared_task
def auto_approve_emergency_task():
    """موافقة تلقائية على الطلبات الطارئة"""
    count = auto_approve_emergency_requests()
    return f"Auto-approved {count} emergency requests"

@shared_task
def generate_ai_summary_task():
    """توليد ملخص AI للطلبات المعلقة"""
    summary = summarize_pending_requests()
    return summary