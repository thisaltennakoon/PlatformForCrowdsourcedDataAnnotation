from django.contrib import admin
from .models import DataAnnotationResult,DataGenerationResult

# Register your models here.
admin.site.register(DataAnnotationResult)
admin.site.register(DataGenerationResult)