from django.db import models

class User1(models.Model):
    first_name = models.CharField(max_length=255,default='')
    last_name = models.CharField(max_length=255,default='')
    email=models.EmailField(default='none@email.com')
    country = models.CharField(max_length=255,default='')
    field = models.CharField(max_length=255,default='')
class Task(models.Model):
    Title = models.CharField(max_length=200, blank=False)
    Description = models.TextField(max_length=256,blank=True)
    DataInstanceAnnotationTimes = models.IntegerField(default = 1)
    def __str__(self):  # display book name in admin panel
        return self.Title

class AnnotationTest(models.Model):
    TaskID = models.ForeignKey(Task,on_delete=models.CASCADE)

class TestResult(models.Model):
    testID = models.ForeignKey(AnnotationTest,on_delete= models.CASCADE)
    annotatorID = models.ForeignKey(User1,on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5,decimal_places=2)