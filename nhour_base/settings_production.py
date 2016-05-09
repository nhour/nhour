import os

from .settings import *

DEBUG = False
SECRET_KEY = os.environ['NHOUR_SECRET_KEY']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
