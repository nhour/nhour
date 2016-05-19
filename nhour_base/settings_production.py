import os

from .settings import *

DEBUG = False
SECRET_KEY = os.environ['NHOUR_SECRET_KEY']
DB_PASSWORD = os.environ['NHOUR_DB_PASSWORD']
DB_USER = os.environ['NHOUR_DB_USER']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nhour',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
