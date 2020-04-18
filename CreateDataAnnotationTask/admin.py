from django.contrib import admin
from .models import Task,DataClass,DataAnnotation

admin.site.register(Task)
admin.site.register(DataClass)
admin.site.register(DataAnnotation)
