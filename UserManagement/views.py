from django.shortcuts import render,redirect,reverse
#from .models import DataGenerationResult
from django.http import HttpResponse
#from CreateDataGenerationTask.models import Task,DataGeneration
#from .models import DataGenerationResult
from django.contrib import messages
#import random
from CreateDataGenerationTask.models import Task as DataGenerationTask
from CreateDataAnnotationTask.models import Task as DataAnnotationTask


def Sign_in(request):
    if request.method == 'POST':
        request.session['user_id'] = request.POST['user_id']
        request.session['password'] = request.POST['password']
        return redirect('/UserManagement/MyTasks')
    else:
        return render(request, 'UserManagement/Sign_in.html')


def view_my_tasks(request):
    if 'user_id' in request.session:
        return render(request, 'UserManagement/test.html' , {'data_generation_tasks': DataGenerationTask.objects.all(),
                                                         'data_annotation_tasks':DataAnnotationTask.objects.all(),
                                                             'user_id':request.session['user_id']})
    else:
        return redirect('/UserManagement/SignIn')


