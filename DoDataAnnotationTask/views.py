from django.shortcuts import render, redirect, reverse
from .models import DataAnnotationResult
from django.http import HttpResponse
from CreateDataAnnotationTask.models import Task, DataClass, AnnotationDataSet
from .models import DataAnnotationResult
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from UserManagement.models import ContributorTask
from django.db import DatabaseError, transaction

def test(request):
    return render(request, 'test.html')

@login_required(login_url='UserManagement:sign_in')
def first(request):
    all_user_annotation_tasks = ContributorTask.objects.filter(UserID_id=request.session['user_id'],
                                                               is_data_annotation_task=True,
                                                               is_data_generation_task=False)
    user_data_annotation_tasks = []
    for annotation_task in all_user_annotation_tasks:
        user_data_annotation_tasks += [annotation_task.TaskID]
    return render(request, 'DoDataAnnotationTask/MyDataAnnotationTasks.html', {'tasks': Task.objects.filter(id__in=user_data_annotation_tasks)}, )


@login_required(login_url='UserManagement:sign_in')
def task(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        data_class = request.POST['data_class']
        data_instance = request.POST['DataInstance']
        task_id = request.POST['task_id']
        annotating_data_instance = AnnotationDataSet.objects.get(TaskID=task_id, DataInstance=data_instance)
        if annotating_data_instance.NumberOfAnnotations < Task.objects.get(id=task_id).DataInstanceAnnotationTimes:  #for extra protection.Can be removed if nessasary
            data_annotation_result = DataAnnotationResult(TaskID=Task.objects.get(id=task_id),
                                                          DataInstance=data_instance,
                                                          ClassName=data_class,
                                                          UserID=user_id)
            data_annotation_result.save()
            annotating_data_instance.NumberOfAnnotations += 1
            annotating_data_instance.save()
            return redirect('/DoDataAnnotationTask/Task?task_id=' + str(task_id))
        else:
            return HttpResponse('error')

    else:
        try:
            task_id = request.GET['task_id']
            data_instance_annotation_times = int(Task.objects.get(id=task_id).DataInstanceAnnotationTimes)
            annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
            data_instances_to_exclude = []
            for i in annotated_data_instances:
                data_instances_to_exclude += [i.DataInstance]
            try:
                with transaction.atomic():
                    data_annotation = AnnotationDataSet.objects.filter(TaskID=task_id,is_viewing=False,NumberOfAnnotations__lt=data_instance_annotation_times).exclude(DataInstance__in=data_instances_to_exclude)
                    if len(data_annotation) > 0:
                        data_instance = random.choice(data_annotation)
                        data_instance_about_to_annotate = AnnotationDataSet.objects.get(TaskID=task_id, DataInstance=data_instance.DataInstance)
                        data_instance_about_to_annotate.is_viewing=True
                        data_instance_about_to_annotate.save()
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    else:
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False,})
            except DatabaseError:
                return HttpResponse("DatabaseError")
        except:
            return redirect('/DoDataAnnotationTask/')


@login_required(login_url='UserManagement:sign_in')
def view_my_annotations(request):
    try:
        task_id = request.GET['task_id']
        user_id = request.session['user_id']
        annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
        if len(annotated_data_instances) > 0:
            return render(request, 'DoDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': True,
                                                               'task_object': Task.objects.get(id=task_id),
                                                               'annotated_data_instances':annotated_data_instances},)
        else:
            return render(request, 'DoDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': False,
                                                               'task_object': Task.objects.get(id=task_id), })
    except:
        return redirect('/DoDataAnnotationTask/')

@login_required(login_url='UserManagement:sign_in')
def view_my_annotations_change(request):
    if request.method == 'POST':
        annotated_data_instance_id = request.POST['annotated_data_instance_id']
        data_class = request.POST['data_class']
        data_annotation_result_not_updated = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = data_annotation_result_not_updated.TaskID_id
        data_annotation_result_not_updated.ClassName = data_class
        data_annotation_result_not_updated.save()
        return redirect('/DoDataAnnotationTask/ViewMyAnnotations?task_id=' + str(task_id))
    else:
        annotated_data_instance_id = request.GET['annotated_data_instance_id']
        annotated_data_instance = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = annotated_data_instance.TaskID_id
        data_instance = AnnotationDataSet.objects.get(TaskID= task_id ,
                                                   DataInstance = annotated_data_instance.DataInstance)
        return render(request, 'DoDataAnnotationTask/ViewMyAnnotationsChange.html',{'annotated_data_instance':annotated_data_instance,
                                                                                    'annotated_data_instance_id':annotated_data_instance_id,
                                                                                     'data_instance':data_instance,
                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                     'data_classes': DataClass.objects.filter(TaskID=task_id),})

"""def view_my_annotations_delete(request):
    annotated_data_instance_id = request.GET['annotated_data_instance_id']
    task_id = DataAnnotationResult.objects.get(id=annotated_data_instance_id).TaskID_id
    try:
        last_confirmation = request.GET['last_confirmation']
        if last_confirmation=="True":
            DataAnnotationResult.objects.get(id=annotated_data_instance_id).delete()
            return redirect('/DoDataAnnotationTask/ViewMyAnnotations?task_id='+str(task_id))
        else:
            return redirect('/DoDataAnnotationTask/ViewMyAnnotations/Change?annotated_data_instance_id=' + str(annotated_data_instance_id))

    except:
        return render(request, 'DoDataAnnotationTask/ViewMyAnnotationsDelete.html', {'annotated_data_instance_id': annotated_data_instance_id,
                                                                                     'task_object':Task.objects.get(id=task_id)})"""
