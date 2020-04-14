from django.shortcuts import render,redirect,reverse
from .models import DataAnnotationResult
from django.http import HttpResponse
from CreateDataAnnotationTask.models import Task,DataClass,DataAnnotation
from DoDataAnnotationTask.models import DataAnnotationResult
from django.contrib import messages
import random

def task(request):
    if request.method == 'POST':
        data_class = request.POST['data_class']
        data_instance = request.POST['DataInstance']
        task_id = request.POST['task_id']
        user_id = request.POST['user_id']
        data_annotation_result = DataAnnotationResult(TaskID = Task.objects.get(id=task_id),
                                                      DataInstance = data_instance,
                                                      ClassName = data_class,
                                                      UserID = user_id)
        data_annotation_result.save()
        return redirect('/DoDataAnnotationTask/Task?id='+str(task_id))
    else :
        try:
            task_id = request.GET['id']
            user_id = 1
            AnnotatedDataInstances = DataAnnotationResult.objects.filter(TaskID=task_id , UserID=user_id)
            DataInstancesToExclude = []
            for i in AnnotatedDataInstances:
                DataInstancesToExclude+=[i.DataInstance]
            data_annotation = DataAnnotation.objects.filter(TaskID=task_id).exclude(DataInstance__in = DataInstancesToExclude)
            if len(data_annotation) > 0:
                DataInstance = random.choice(data_annotation)
                return render(request , 'Task.html',{'taskobject':Task.objects.get(id=task_id),
                                                     'dataclasses':DataClass.objects.filter(TaskID=task_id),
                                                     'data_instance':DataInstance,
                                                     'user_id':user_id,
                                                     'task_id':task_id},)
            else:
                #messages.info(request , "<h2>Congratulations!</h2> <h3><br>All the data instances in this task has been annotated.Try another task</h3>")
                return HttpResponse("<h2>Congratulations!</h2> <h3><br>All the data instances in this task has been annotated.Try another task</h3>")
        except:
            return redirect('/DoDataAnnotationTask/')



def task1(request):
    id = request.GET['id']
    #if request.method == 'POST':


    #userid = 1
    #AnnotatedDataInstances = DataAnnotationResult.objects.filter(TaskID=id , UserID=userid)
    #DataInstancesToExclude = []
    #for i in AnnotatedDataInstances:
        #DataInstancesToExclude+=[i.DataInstance]
    dataannotation = DataAnnotation.objects.filter(TaskID=id)
    """data_instance_list = []
    for datainstance in dataannotation:
        a = str(datainstance.DataInstance)
        data_instance_list += [a[7:]]"""
    #DataInstance = str(dataannotation.DataInstance)[7:]


    return render(request , 'Task1.html',{'taskobject':Task.objects.get(id=id),
                                         'dataclasses':DataClass.objects.filter(TaskID=id),
                                         'data_instance_list':dataannotation},)

def first(request):
    return render(request , 'DoDataAnnotationTask.html',{'tasks':Task.objects.all()},)
