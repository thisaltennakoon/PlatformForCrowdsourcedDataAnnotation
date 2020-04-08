from django.shortcuts import render
from .models import DataAnnotationResult
from django.http import HttpResponse
from CreateDataAnnotationTask.models import Task,DataClass,DataAnnotation


def first(request):
    return render(request , 'DoDataAnnotationTask.html',{'tasks':Task.objects.all()},)



def task(request):
    id = request.GET['id']
    dataannotation = DataAnnotation.objects.filter(TaskID=id)
    data_instance_list = []
    for datainstance in dataannotation:
        a = str(datainstance.DataInstance)
        data_instance_list += [a[7:]]


    return render(request , 'Task.html',{'taskobject':Task.objects.get(id=id),
                                         'dataclasses':DataClass.objects.filter(TaskID=id),
                                         'data_instance_list':data_instance_list},)


