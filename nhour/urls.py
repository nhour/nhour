from django.conf.urls import url

from django.contrib import admin

from nhour import models
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^edit/([0-9]{4})/([0-9]{1,2})/([0-9]*)$', views.edit_week, name='edit_week'),
    url(r'^$', views.index_redirect),
]
