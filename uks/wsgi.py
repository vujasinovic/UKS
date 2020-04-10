"""
WSGI config for uks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from github_sync.github_sync import setup_sync_scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uks.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_wsgi_application()

setup_sync_scheduler()
