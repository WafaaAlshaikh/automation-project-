from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, LeaveRequestViewSet, AIChatViewSet

# إنشاء Router
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leaverequest')
router.register(r'ai', AIChatViewSet, basename='ai')

urlpatterns = [
    path('', include(router.urls)),
]