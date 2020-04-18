from django.db import models
from CreateDataGenerationTask.models import Task


class DataGenerationResult(models.Model):
    TaskID = models.ForeignKey(Task , on_delete=models.CASCADE)
    DataInstance = models.CharField(max_length=30, blank=False )
    GenerationResult = models.CharField(max_length=400, blank=False)
    #ClassName = models.ForeignKey(DataClass , on_delete=models.CASCADE)
    UserID = models.IntegerField(null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)

    #def __str__(self):  # display book name in admin panel
        #return self.DataInstance