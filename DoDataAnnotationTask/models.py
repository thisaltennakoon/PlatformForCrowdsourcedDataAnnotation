from django.db import models
from CreateTask.models import Task


class DataAnnotationResult(models.Model):
    TaskID = models.ForeignKey(Task , on_delete=models.CASCADE)
    DataInstance = models.CharField(max_length=30, blank=False)
    ClassID = models.IntegerField(default=0, null=False, blank=False)
    #ClassName = models.CharField(max_length=100, blank=False)
    #ClassName = models.ForeignKey(DataClass , on_delete=models.CASCADE)
    UserID = models.IntegerField(null=False,blank=False)
    LastUpdate = models.DateTimeField(auto_now=True)

    #def __str__(self):  # display book name in admin panel
        #return 'TaskID:'+str(self.TaskId) + ' DataInstance:' + self.DataInstance + ' UserID:'+self.UserID + ' ClassName:' + self.ClassName
