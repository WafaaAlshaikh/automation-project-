import os
import json
from employees.models import LeaveRequest, Employee
from django.utils import timezone

# Note: You'll need to install: pip install openai
# Then get your API key from: https://platform.openai.com/api-keys

def summarize_leave_requests_with_ai():
    """
    Use OpenAI/Claude to summarize pending leave requests.
    This is a mock version - you'll need to add your API key.
    """
    pending_requests = LeaveRequest.objects.filter(status='PENDING')
    
    if not pending_requests:
        return "No pending leave requests today. ✅"
    
    # Prepare data for AI
    requests_data = []
    for req in pending_requests:
        requests_data.append({
            'employee': f"{req.employee.user.first_name} {req.employee.user.last_name}",
            'department': req.employee.department,
            'type': req.get_leave_type_display(),
            'start_date': str(req.start_date),
            'end_date': str(req.end_date),
            'days': req.days_count,
            'reason': req.reason
        })
    
    prompt = f"""
    Summarize these leave requests for a manager:
    {json.dumps(requests_data, indent=2)}
    
    Please provide:
    1. Total number of requests
    2. Breakdown by department
    3. Any urgent or unusual requests
    4. Recommendations
    """
    
    # For demo, return a mock response
    # In production with real API:
    # import openai
    # openai.api_key = os.environ.get('OPENAI_API_KEY')
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content
    
    mock_summary = f"""
📝 AI SUMMARY - {timezone.now().date()}
{'='*40}

Total Pending Requests: {len(requests_data)}

Department Breakdown:
- Engineering: {sum(1 for r in requests_data if r['department'] == 'Engineering')} requests
- HR: {sum(1 for r in requests_data if r['department'] == 'HR')} requests

Key Requests:
1. {requests_data[0]['employee']} - {requests_data[0]['type']} ({requests_data[0]['days']} days)
   Reason: {requests_data[0]['reason']}

Recommendations:
- All requests appear reasonable
- Consider approving emergency requests ASAP
"""
    return mock_summary

def get_ai_approval_recommendation(leave_request_id):
    """Get AI recommendation for a specific leave request"""
    try:
        req = LeaveRequest.objects.get(id=leave_request_id)
    except LeaveRequest.DoesNotExist:
        return "Request not found"
    
    prompt = f"""
    Leave Request Details:
    Employee: {req.employee.user.first_name} {req.employee.user.last_name}
    Department: {req.employee.department}
    Type: {req.get_leave_type_display()}
    Duration: {req.days_count} days
    Reason: {req.reason}
    
    Should this request be approved? Consider:
    - Leave type
    - Department workload
    - Employee history
    Provide recommendation (Approve/Reject) and reason.
    """
    
    # Mock response
    if req.days_count <= 3:
        return f"✅ APPROVED: Short leave request ({req.days_count} days) is reasonable."
    else:
        return f"⚠️ REVIEW: Long leave request ({req.days_count} days). Check with manager."