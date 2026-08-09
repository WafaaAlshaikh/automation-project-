import os
import json
from django.conf import settings
from employees.models import LeaveRequest
from django.utils import timezone
import json

# محاولة استيراد Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Groq not installed. Run: pip install groq")

class GroqAIService:
    """Service class for interacting with Groq API"""
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', getattr(settings, 'GROQ_API_KEY', None))
        self.model = os.environ.get('GROQ_MODEL', 'llama3-70b-8192')
        
        if not self.api_key:
            print("⚠️ GROQ_API_KEY not set. AI features will use mock responses.")
            self.client = None
        elif not GROQ_AVAILABLE:
            print("⚠️ Groq library not installed.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
    
    def get_response(self, messages, temperature=0.7, max_tokens=500):
        """Send messages to Groq API and get response"""
        if not self.client:
            return self._get_mock_response(messages)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            return f"⚠️ AI Error: {str(e)}"
    
    def _get_mock_response(self, messages):
        """Fallback mock response when API key is missing"""
        return f"[MOCK] AI would respond to: {messages[-1]['content'][:100]}..."

# Initialize global service
groq_service = GroqAIService()

def summarize_pending_requests():
    """Generate AI summary of pending leave requests"""
    pending = LeaveRequest.objects.filter(status='PENDING')
    
    if not pending:
        return "✅ No pending leave requests today!"
    
    requests_data = []
    for req in pending:
        requests_data.append({
            'employee': f"{req.employee.user.first_name} {req.employee.user.last_name}",
            'department': req.employee.department,
            'type': req.get_leave_type_display(),
            'days': req.days_count,
            'reason': req.reason
        })
    
    system_prompt = """You are an AI assistant helping a manager review leave requests.
    Provide a clear summary with:
    1. Total count
    2. Breakdown by department
    3. Urgent cases
    4. Recommendations
    Be concise."""
    
    user_prompt = f"Pending leave requests:\n{json.dumps(requests_data, indent=2)}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = groq_service.get_response(messages, temperature=0.3, max_tokens=600)
    
    return f"📊 **AI Summary - {timezone.now().date()}**\n\n{response}"

def get_ai_approval_recommendation(leave_request_id):
    """Get AI recommendation for a specific leave request"""
    try:
        req = LeaveRequest.objects.get(id=leave_request_id)
    except LeaveRequest.DoesNotExist:
        return {"error": "Request not found"}
    
    request_data = {
        'employee': f"{req.employee.user.first_name} {req.employee.user.last_name}",
        'department': req.employee.department,
        'leave_type': req.get_leave_type_display(),
        'days': req.days_count,
        'reason': req.reason
    }
    
    system_prompt = """You are an AI assistant for HR.
    Analyze the leave request and provide recommendation.
    Format as JSON with: recommendation (Approve/Reject/Review), reasoning, risk_level (Low/Medium/High)."""
    
    user_prompt = f"Evaluate this request:\n{json.dumps(request_data, indent=2)}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = groq_service.get_response(messages, temperature=0.3, max_tokens=300)
    
    try:
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            return json.loads(response[json_start:json_end])
    except:
        pass
    
    return {
        "recommendation": "REVIEW",
        "reasoning": response[:200],
        "risk_level": "MEDIUM"
    }

def auto_evaluate_requests() -> dict:
    """تقييم تلقائي للطلبات المعلقة"""
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

def summarize_leave_requests_with_ai():
    """Alias for summarize_pending_requests for backward compatibility"""
    return summarize_pending_requests()