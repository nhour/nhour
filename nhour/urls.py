from django.contrib.auth.views import login, logout_then_login
from django.conf.urls import url, include
from django.contrib import admin

from nhour import models
from . import views

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^delete/([0-9]{4})/([0-9]{1,2})/([0-9]*)/([0-9]*)$', views.delete_entry, name='delete'),
    url(r'^edit/([0-9]{4})/([0-9]{1,2})/([0-9]*)$', views.edit_week, name='edit_week'),
    url(r'^$', views.index_redirect),
    url(r'^logout/', logout_then_login, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^admin/', admin.site.urls),
]
