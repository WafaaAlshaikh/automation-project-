from django.core.management.base import BaseCommand
from automation.scripts import send_daily_report_email, auto_approve_emergency_requests
from automation.ai_integration import summarize_leave_requests_with_ai

class Command(BaseCommand):
    help = 'Send daily leave report and process emergency requests'

    def handle(self, *args, **options):
        self.stdout.write('📊 Processing daily automation...')
        
        # Auto-approve emergencies
        count = auto_approve_emergency_requests()
        self.stdout.write(f'✅ Auto-approved {count} emergency requests')
        
        # Generate AI summary
        summary = summarize_leave_requests_with_ai()
        self.stdout.write('\n' + summary)
        
        # Send report
        report = send_daily_report_email()
        self.stdout.write('✅ Daily report sent successfully!')