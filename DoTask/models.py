from django.db import models
from CreateTask.models import Task


class DataAnnotationResult(models.Model):
    TaskID = models.CharField(max_length=30, blank=False)
    DataInstance = models.CharField(max_length=30, blank=False)
    ClassID = models.IntegerField(default=0, null=False, blank=False)
    UserID = models.IntegerField(null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)


class DataGenerationResult(models.Model):
    TaskID = models.CharField(max_length=30, blank=False)
    DataInstance = models.CharField(max_length=30, blank=False )
    GenerationResult = models.CharField(max_length=400, blank=False)
    UserID = models.IntegerField(null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)