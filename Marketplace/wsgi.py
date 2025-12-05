"""
WSGI config for Marketplace project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# مسیر پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Marketplace.settings')

application = get_wsgi_application()

# WhiteNoise برای سرو فایل‌های استاتیک
application = WhiteNoise(application, root=str(BASE_DIR / "staticfiles"), prefix="static/")
