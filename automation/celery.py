import os
from celery import Celery

# تعيين متغير البيئة لإعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# إنشاء تطبيق Celery
app = Celery('automation')

# تحميل الإعدادات من Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام تلقائياً من جميع التطبيقات
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')