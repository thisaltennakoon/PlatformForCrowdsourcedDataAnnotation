from django.contrib import admin
from .models import Task,DataClass,AnnotationDataSet

admin.site.register(Task)
admin.site.register(DataClass)
admin.site.register(AnnotationDataSet)
