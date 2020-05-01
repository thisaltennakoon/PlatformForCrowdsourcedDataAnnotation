
from django.db import models
from django.urls import reverse
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile

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
    is_correct = models.BooleanField(default=False)



    

# class DataSetImage(models.Model):
#     taskID = models.ForeignKey(AnnotationTask, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="uploads", height_field=None, width_field=None, max_length=None)


# class ExampleImage(models.Model):
#     taskID = models.ForeignKey(AnnotationTask, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='examples', verbose_name='Image')

# class ExampleResults(models.Model):
#     imageID = models.ForeignKey(ExampleImage, on_delete=models.CASCADE)
#     cateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)

class GenerationTask(models.Model):
    creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
    instructions = models.CharField(max_length=1000)



class GenerationClass(models.Model):
    TaskID = models.ForeignKey(GenerationTask,on_delete=models.CASCADE)
    classtitle = models.CharField(max_length=1000)
    requiredDataType = models.CharField(max_length=1,default='T') #Text:T or image:I

class GenerationExamplesText(models.Model):
    ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
    example = models.CharField(max_length=2000)

# class GenerationExamplesImage(models.Model):
#     ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
#     example = models.ImageField()