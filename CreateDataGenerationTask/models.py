from django.db import models


class Task(models.Model):
    Title = models.CharField(max_length=200, blank=False)
    Description = models.TextField(max_length=256, blank=True)
    DataInstanceGenerationTimes = models.IntegerField(default=1)
    def __str__(self):  # display book name in admin panel
        return self.Title



class DataGeneration(models.Model):
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    DataInstance = models.CharField(max_length=400, blank=False , unique=True)
    NumberOfGenerations = models.IntegerField(default=0)
    def __str__(self):  # display book name in admin panel
        return self.DataInstance



