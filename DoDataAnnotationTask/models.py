from django.db import models


class DataAnnotationResult(models.Model):
    TaskId = models.IntegerField(null=False,blank=False)
    DataInstance = models.CharField(max_length=30, blank=False)
    ClassName = models.CharField(max_length=100, blank=False)
    UserID = models.IntegerField(null=False,blank=False)

    #def __str__(self):  # display book name in admin panel
        #return 'TaskID:'+str(self.TaskId) + ' DataInstance:' + self.DataInstance + ' UserID:'+self.UserID + ' ClassName:' + self.ClassName
