from django.contrib import admin

from .models import System, Task, Project, RegularEntry, SpecialEntry, Activity

admin.site.register(System)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(RegularEntry)
admin.site.register(SpecialEntry)
admin.site.register(Activity)
