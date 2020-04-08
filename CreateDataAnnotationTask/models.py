from django.db import models


class Task(models.Model):
    Title = models.CharField(max_length=200, blank=False)
    Description = models.TextField(max_length=256,blank=True)
    def __str__(self):  # display book name in admin panel
        return self.Title


class DataClass(models.Model):
    TaskID = models.ForeignKey(Task , on_delete=models.CASCADE)
    ClassName = models.CharField(max_length=100, blank=False)
    def __str__(self):  # display book name in admin panel
        return self.ClassName


class DataAnnotation(models.Model):
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    DataInstance = models.ImageField(upload_to='static/img/',blank=False,  )
    #def __str__(self):  # display book name in admin panel
        #return self.TaskID


