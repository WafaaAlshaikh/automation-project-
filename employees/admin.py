from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Employee, LeaveRequest
from automation.tasks import send_daily_report_email_task, auto_approve_emergency_task, generate_ai_summary_task

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'Employee Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (EmployeeInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'department', 'position', 'hire_date']
    list_filter = ['department', 'position']
    search_fields = ['user__first_name', 'user__last_name', 'department']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'leave_type', 'status', 'start_date', 'end_date', 'days_count']
    list_filter = ['status', 'leave_type', 'start_date']
    search_fields = ['employee__user__first_name', 'employee__user__last_name', 'reason']
    readonly_fields = ['created_at', 'updated_at', 'approval_date']
    
    actions = ['approve_selected', 'reject_selected', 'send_ai_summary']
    
    def approve_selected(self, request, queryset):
        for req in queryset:
            if req.status == 'PENDING':
                req.status = 'APPROVED'
                req.approval_date = timezone.now()
                req.save()
        self.message_user(request, f'Approved {queryset.count()} requests')
    approve_selected.short_description = 'Approve selected requests'
    
    def reject_selected(self, request, queryset):
        for req in queryset:
            if req.status == 'PENDING':
                req.status = 'REJECTED'
                req.save()
        self.message_user(request, f'Rejected {queryset.count()} requests')
    reject_selected.short_description = 'Reject selected requests'
    
    def send_ai_summary(self, request, queryset):
        task = generate_ai_summary_task.delay()
        self.message_user(request, f'AI summary generated! Task ID: {task.id}')
    send_ai_summary.short_description = 'Generate AI Summary'