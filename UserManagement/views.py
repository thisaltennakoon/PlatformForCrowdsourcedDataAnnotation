from django.shortcuts import render,redirect,reverse
#from .models import DataGenerationResult
from django.http import HttpResponse
#from CreateDataGenerationTask.models import Task,DataGeneration
#from .models import DataGenerationResult
from django.contrib import messages
#import random
from CreateDataGenerationTask.models import Task as DataGenerationTask
from CreateDataAnnotationTask.models import Task as DataAnnotationTask


def view_my_tasks(request):
    return render(request, 'UserManagement/test.html' , {'data_generation_tasks': DataGenerationTask.objects.all(),
                                                         'data_annotation_tasks':DataAnnotationTask.objects.all()})


