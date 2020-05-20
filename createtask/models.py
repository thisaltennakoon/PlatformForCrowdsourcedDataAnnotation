
from django.db import models
from django.urls import reverse
from django.core.files.base import ContentFile
from django.conf import settings
from zipfile import ZipFile

class UserNew2(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=64)



#IMAGE ANNOTATION AND 'DATA GENARATION'

class Task(models.Model):
    creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
    instructions = models.CharField(max_length=1000)
    taskType = models.CharField(max_length=10) #TextAnno,ImgAnno,TextGen,ImgGen
    requiredNumofAnnotations = models.IntegerField(default=1) 
    
class Cateogary(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    cateogaryName = models.CharField(max_length= 250)
    cateogaryTag = models.IntegerField(default=0) #0,1,2,..

def directory_path2(instance,filename):
    return 'MediaAnno/task_{0}/{1}'.format(instance.taskID.id, filename)
class MediaDataInstance(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    media = models.FileField(upload_to=directory_path2)


#TEXT ANNOTATIONS
def directory_path(instance,filename):
    return 'TextAnno/task_{0}/{1}'.format(instance.taskID.id, filename)
class TextFile(models.Model):
    taskID = models.ForeignKey(Task,on_delete=models.CASCADE)
    csvFile = models.FileField(upload_to=directory_path)

class TextDataInstance(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)

class TextData(models.Model):
    InstanceID = models.ForeignKey(TextDataInstance, on_delete=models.CASCADE)
    Data = models.CharField(max_length=3000)


#QUIZ
class Questionaire(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
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
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="uploads", height_field=None, width_field=None, max_length=None)


# class ExampleImage(models.Model):
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='examples', verbose_name='Image')

# class ExampleResults(models.Model):
#     imageID = models.ForeignKey(ExampleImage, on_delete=models.CASCADE)
#     cateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)

# class GenerationTask(models.Model):
#     creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.CharField(max_length=1000)
#     status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
#     instructions = models.CharField(max_length=1000)



# class GenerationClass(models.Model):
#     TaskID = models.ForeignKey(GenerationTask,on_delete=models.CASCADE)
#     classtitle = models.CharField(max_length=1000)
#     requiredDataType = models.CharField(max_length=1,default='T') #Text:T or image:I dont need?

# class GenerationExamplesText(models.Model):
#     ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
#     example = models.CharField(max_length=2000)

# class GenerationExamplesImage(models.Model):
#     ClassID = models.ForeignKey(GenerationClass,on_delete=models.CASCADE)
#     example = models.ImageField()



#TEXT DATA ANNOTATION

# class TextTask(models.Model):
#     creatorID = models.ForeignKey(UserNew2,on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.CharField(max_length=1000)
#     status = models.CharField(max_length=60, default='new')    #new,#inprogress,#completed
#     instructions = models.CharField(max_length=1000)
#     #csvFile = models.FileField(upload_to=directory_path)



# class TextCateogary(models.Model):
#     taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
#     cateogaryName = models.CharField(max_length= 250)




#TEXT DATA EXAMPLE AND TEST
class CateogaryTag(models.Model):
    CateogaryID = models.ForeignKey(Cateogary, on_delete=models.CASCADE)
    TagNumber = models.IntegerField(max_length=2)

class AnnotationTest(models.Model):
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)

class ExampleTextDataInstance(models.Model):
    testID = models.ForeignKey(AnnotationTest, on_delete=models.CASCADE)

class ExampleTextData(models.Model):
    InstanceID = models.ForeignKey(ExampleTextDataInstance, on_delete=models.CASCADE)
    Data = models.CharField(max_length=3000)

class ExampleTextAnnoResult(models.Model):
    ExampleTextDataInstanceID = models.ForeignKey(ExampleTextDataInstance, on_delete=models.CASCADE)
    resultCateogary = models.ForeignKey(Cateogary, on_delete=models.CASCADE)
    