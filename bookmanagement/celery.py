from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Đặt biến môi trường cho Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmanagement.settings')

# Tạo app Celery
app = Celery('bookmanagement')

# Đọc cấu hình từ Django settings, prefix "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Tự động load các task từ tất cả các app Django
app.autodiscover_tasks()
