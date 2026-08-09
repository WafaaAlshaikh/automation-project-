import os
from groq import Groq
from typing import List, Dict, Optional
import json

class GroqAIClient:
    """عميل للتواصل مع Groq AI - مجاني وسريع"""
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
        self.default_model = "llama-3.3-70b-versatile"  # أفضل نموذج مجاني
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        توليد استجابة من Groq AI
        
        Args:
            prompt: سؤال أو طلب المستخدم
            system_prompt: توجيهات للنظام (اختياري)
        
        Returns:
            نص الاستجابة
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def analyze_leave_request(self, request_data: Dict) -> Dict:
        """
        تحليل طلب إجازة وتقديم توصية
        
        Args:
            request_data: بيانات طلب الإجازة
        
        Returns:
            توصية مع تحليل
        """
        prompt = f"""
        Analyze this leave request and provide a recommendation:
        
        Employee: {request_data.get('employee', 'Unknown')}
        Department: {request_data.get('department', 'Unknown')}
        Leave Type: {request_data.get('leave_type', 'Unknown')}
        Duration: {request_data.get('days', 0)} days
        Reason: {request_data.get('reason', 'No reason provided')}
        
        Provide:
        1. Recommendation (Approve/Reject/Review)
        2. Reasoning (why)
        3. Risk Level (Low/Medium/High)
        4. Suggested action for manager
        
        Format as JSON.
        """
        
        system_prompt = """
        You are an HR assistant specialized in leave management.
        Provide professional, balanced recommendations.
        Consider:
        - Department workload (assume normal)
        - Leave type appropriateness
        - Duration reasonableness
        - Employee history (assume good standing)
        """
        
        response = self.generate_response(prompt, system_prompt)
        
        # محاولة تحويل الرد إلى JSON
        try:
            # استخراج JSON من النص
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        # رد بديل إذا لم ينجح التحويل
        return {
            "recommendation": "REVIEW",
            "reasoning": response[:200],
            "risk_level": "MEDIUM",
            "suggested_action": "Review with manager"
        }
    
    def summarize_requests(self, requests: List[Dict]) -> str:
        """
        تلخيص طلبات الإجازات المتعددة
        
        Args:
            requests: قائمة طلبات الإجازات
        
        Returns:
            تلخيص مفيد للمدير
        """
        if not requests:
            return "No pending requests today. ✅"
        
        data = json.dumps(requests, indent=2, ensure_ascii=False)
        
        prompt = f"""
        Summarize these leave requests for a manager:
        
        {data}
        
        Provide:
        1. Total count
        2. Breakdown by department
        3. Urgent cases
        4. Recommendations
        """
        
        system_prompt = """
        You are a concise assistant for HR managers.
        Provide clear, actionable summaries.
        Highlight any issues or patterns.
        """
        
        return self.generate_response(prompt, system_prompt)