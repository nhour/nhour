from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

from . import views

urlpatterns = [
    url(r'^login', login, name='login'),
    url(r'^delete/([0-9]*)/$', views.delete_entry, name='delete_entry'),
    url(r'^edit/([0-9]{4})/([0-9]{1,2})/([0-9]*)/$', views.edit_week, name='edit_week'),
    url(r'^save/([0-9]*)/$', views.save_entry, name="save_entry"),
    url(r'^create/$', views.create_entry, name="create_entry"),
    url(r'^$', views.index_redirect),
    url(r'^logout/', logout_then_login, name="logout"),
    url(r'^register/$', views.register, name="register"),
    url(r'^admin/', admin.site.urls),
    url(r'^thanks/', views.thank_you, name="thanks")
]
