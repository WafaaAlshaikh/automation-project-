from .groq_client import GroqAIClient
from employees.models import LeaveRequest, Employee
from django.utils import timezone
import json

groq_client = GroqAIClient()

def get_ai_approval_recommendation(leave_request_id: int) -> dict:
    try:
        req = LeaveRequest.objects.get(id=leave_request_id)
        
        request_data = {
            'employee': f"{req.employee.user.first_name} {req.employee.user.last_name}",
            'department': req.employee.department,
            'leave_type': req.get_leave_type_display(),
            'days': req.days_count,
            'reason': req.reason
        }
        
        return groq_client.analyze_leave_request(request_data)
        
    except LeaveRequest.DoesNotExist:
        return {"error": "Request not found"}

def summarize_pending_requests() -> str:
    pending = LeaveRequest.objects.filter(status='PENDING')
    
    requests_data = []
    for req in pending:
        requests_data.append({
            'employee': f"{req.employee.user.first_name} {req.employee.user.last_name}",
            'department': req.employee.department,
            'type': req.get_leave_type_display(),
            'days': req.days_count,
            'reason': req.reason
        })
    
    return groq_client.summarize_requests(requests_data)

def auto_evaluate_requests() -> dict:
    pending = LeaveRequest.objects.filter(status='PENDING')
    
    results = {
        'total': pending.count(),
        'approved': 0,
        'rejected': 0,
        'review': 0,
        'details': []
    }
    
    for req in pending:
        rec = get_ai_approval_recommendation(req.id)
        
        if rec.get('recommendation') == 'APPROVE':
            results['approved'] += 1
        elif rec.get('recommendation') == 'REJECT':
            results['rejected'] += 1
        else:
            results['review'] += 1
        
        results['details'].append({
            'request_id': req.id,
            'employee': str(req.employee),
            'recommendation': rec.get('recommendation', 'REVIEW'),
            'reason': rec.get('reasoning', '')
        })
    
    return results

summarize_leave_requests_with_ai = summarize_pending_requests
