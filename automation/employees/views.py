from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Employee, LeaveRequest
from .serializers import EmployeeSerializer, LeaveRequestSerializer
from automation.ai_integration import summarize_leave_requests_with_ai, get_ai_approval_recommendation
from automation.scripts import send_daily_report_email, auto_approve_emergency_requests
from rest_framework.permissions import IsAuthenticated

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny] 

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(status='PENDING')
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        if leave_request.status != 'PENDING':
            return Response({'error': 'This request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        leave_request.status = 'APPROVED'
        leave_request.approval_date = timezone.now()
        leave_request.save()
        
        return Response({'message': 'Leave request approved successfully!'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave_request = self.get_object()
        if leave_request.status != 'PENDING':
            return Response({'error': 'This request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        leave_request.status = 'REJECTED'
        leave_request.save()
        
        return Response({'message': 'Leave request rejected.'})




    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get AI summary of all pending requests"""
        summary = summarize_leave_requests_with_ai()
        return Response({'summary': summary})

    @action(detail=True, methods=['get'])
    def ai_recommendation(self, request, pk=None):
        """Get AI recommendation for a specific request"""
        recommendation = get_ai_approval_recommendation(pk)
        return Response({'recommendation': recommendation})

    @action(detail=False, methods=['post'])
    def send_report(self, request):
        """Send daily report via email"""
        report = send_daily_report_email()
        return Response({'message': 'Report sent successfully!', 'report': report})

    @action(detail=False, methods=['post'])
    def auto_approve_emergency(self, request):
        """Auto-approve emergency requests"""
        count = auto_approve_emergency_requests()
        return Response({'message': f'Auto-approved {count} emergency requests'})