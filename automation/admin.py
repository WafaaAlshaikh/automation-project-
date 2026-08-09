from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.contrib import messages
from django.http import HttpResponse

class AutomationAdminMixin:
    """مixin لإضافة أزرار تشغيل المهام في واجهة الإدارة"""
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('run-daily-report/', self.admin_site.admin_view(self.run_daily_report),
                 name='run-daily-report'),
            path('run-auto-approve/', self.admin_site.admin_view(self.run_auto_approve),
                 name='run-auto-approve'),
            path('run-weekly-summary/', self.admin_site.admin_view(self.run_weekly_summary),
                 name='run-weekly-summary'),
        ]
        return custom_urls + urls
    
    def run_daily_report(self, request):
        """تشغيل التقرير اليومي"""
        try:
            from automation.scripts import send_daily_report_email
            report = send_daily_report_email()
            
            # عرض التقرير في رسالة نجاح
            message = f"📧 Daily report sent successfully!\n\n{report}"
            self.message_user(request, message, level=messages.SUCCESS)
            
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level=messages.ERROR)
        
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))
    
    def run_auto_approve(self, request):
        """تشغيل الموافقة التلقائية على الطلبات الطارئة"""
        try:
            from automation.scripts import auto_approve_emergency_requests
            count = auto_approve_emergency_requests()
            self.message_user(
                request, 
                f"⚡ Auto-approved {count} emergency requests successfully!", 
                level=messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level=messages.ERROR)
        
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))
    
    def run_weekly_summary(self, request):
        """تشغيل التقرير الأسبوعي"""
        try:
            from automation.ai_integration import generate_weekly_insights
            insights = generate_weekly_insights()
            
            # عرض التحليل في رسالة نجاح
            message = f"📊 Weekly summary generated!\n\n{insights}"
            self.message_user(request, message, level=messages.SUCCESS)
            
        except Exception as e:
            self.message_user(request, f"❌ Error: {str(e)}", level=messages.ERROR)
        
        return redirect(request.META.get('HTTP_REFERER', '/admin/'))

# إنشاء موقع إدارة مخصص
class AutomationAdmin(admin.AdminSite):
    """موقع إدارة مخصص للأتمتة"""
    site_header = "🤖 Automation Control Panel"
    site_title = "Automation Admin"
    index_title = "📋 Task Management Dashboard"

# إنشاء كائن الموقع
admin_site = AutomationAdmin(name='automation_admin')

# تسجيل النماذج مع الموقع الجديد (اختياري)
# admin_site.register(Employee, EmployeeAdmin)
# admin_site.register(LeaveRequest, LeaveRequestAdmin)