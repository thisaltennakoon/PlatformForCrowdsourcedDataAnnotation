from django.db import models
from django.urls import reverse

class UserNew2(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=64)

class AnnotationTask(models.Model):
    creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
    instructions = models.CharField(max_length=1000)
    
class Cateogary(models.Model):
    taskID = models.ForeignKey(AnnotationTask, on_delete=models.CASCADE)
    cateogaryName = models.CharField(max_length= 250)

class Questionaire(models.Model):
    taskID = models.ForeignKey(AnnotationTask, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Active')  #ative,#notactive

class McqQuestion(models.Model):
    questionaireID = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)

class DescrptiveQuestion(models.Model):
    questionaireID = models.ForeignKey(Questionaire, on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)

class McqOption(models.Model):
    questionID = models.ForeignKey(McqQuestion, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)

