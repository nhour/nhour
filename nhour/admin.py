from django.contrib import admin

from .models import System, Task, Project

admin.site.register(System)
admin.site.register(Task)
admin.site.register(Project)