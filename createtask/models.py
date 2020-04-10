from django.db import models
from django.core.urlresolvers import reverse

class User(models.Model):
    name = models.CharField(max_length=250)

class AnnotationTask(models.Model):
    creatorID = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    decription = models.CharField(max_length=1000)
    status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
    instructions = models.CharField(max_length=1000)
    