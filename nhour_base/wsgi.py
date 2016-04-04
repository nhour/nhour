"""
WSGI config for tunnit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nhour_base.settings")
os.environ.setdefault("NHOUR_STAGING", "TRUE")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)