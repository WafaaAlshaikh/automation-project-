from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, LeaveRequestSerializer

# استيرادات AI
from automation.ai_integration import (
    groq_service, 
    summarize_leave_requests_with_ai,
    get_ai_approval_recommendation,
    generate_weekly_insights,
    chat_with_ai
)
from automation.scripts import send_daily_report_email, auto_approve_emergency_requests


# ---------- Employee ViewSet ----------
class EmployeeViewSet(viewsets.ModelViewSet):
    """API للموظفين - CRUD كامل"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]  # للتجربة


# ---------- Leave Request ViewSet ----------
class LeaveRequestViewSet(viewsets.ModelViewSet):
    """API لطلبات الإجازات - مع إضافات للموافقة والرفض"""
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        """عند إنشاء طلب جديد، تكون الحالة PENDING افتراضياً"""
        serializer.save(status='PENDING')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """الموافقة على طلب إجازة"""
        leave_request = self.get_object()
        if leave_request.status != 'PENDING':
            return Response(
                {'error': 'This request is not pending'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave_request.status = 'APPROVED'
        leave_request.approval_date = timezone.now()
        leave_request.save()
        
        return Response({'message': 'Leave request approved successfully!'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """رفض طلب إجازة"""
        leave_request = self.get_object()
        if leave_request.status != 'PENDING':
            return Response(
                {'error': 'This request is not pending'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave_request.status = 'REJECTED'
        leave_request.save()
        
        return Response({'message': 'Leave request rejected.'})
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """الحصول على ملخص AI للطلبات المعلقة"""
        summary = summarize_leave_requests_with_ai()
        return Response({'summary': summary})

    @action(detail=True, methods=['get'])
    def ai_recommendation(self, request, pk=None):
        """الحصول على توصية AI لطلب معين"""
        recommendation = get_ai_approval_recommendation(pk)
        return Response({'recommendation': recommendation})

    @action(detail=False, methods=['post'])
    def send_report(self, request):
        """إرسال التقرير اليومي عبر البريد الإلكتروني"""
        report = send_daily_report_email()
        return Response({
            'message': 'Report sent successfully!', 
            'report': report
        })

    @action(detail=False, methods=['post'])
    def auto_approve_emergency(self, request):
        """الموافقة التلقائية على الطلبات الطارئة"""
        count = auto_approve_emergency_requests()
        return Response({
            'message': f'Auto-approved {count} emergency requests'
        })


# ---------- AI Chat ViewSet (منفصل) ----------
class AIChatViewSet(viewsets.ViewSet):
    """AI Chat endpoints باستخدام Groq"""
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """محادثة مع AI"""
        query = request.data.get('query')
        session_id = request.data.get('session_id', 'default')
        
        if not query:
            return Response(
                {'error': 'Query is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response = chat_with_ai(query, session_id)
        return Response({
            'response': response,
            'session_id': session_id
        })
    
    @action(detail=False, methods=['get'])
    def weekly_insights(self, request):
        """الحصول على تحليلات أسبوعية"""
        insights = generate_weekly_insights()
        return Response({'insights': insights})
    
    @action(detail=False, methods=['get'])
    def models(self, request):
        """عرض نماذج Groq المتاحة"""
        if groq_service.client:
            try:
                models = groq_service.client.models.list()
                return Response({
                    'available_models': [
                        m.id for m in models.data if 'groq' in m.id
                    ]
                })
            except Exception as e:
                return Response(
                    {'error': str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {'error': 'Groq client not initialized'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )