from django.contrib import admin

from tasks_app.models import Task, Comment

admin.site.register(Task)
admin.site.register(Comment)

