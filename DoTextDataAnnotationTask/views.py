from django.shortcuts import render, redirect, reverse
from .models import DataAnnotationResult
from django.http import HttpResponse
from CreateTextDataAnnotationTask.models import Task, DataClass, AnnotationDataSet, AnnotationSubDataSet
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
    return render(request, 'DoTextDataAnnotationTask/MyDataAnnotationTasks.html', {'tasks': Task.objects.filter(id__in=user_data_annotation_tasks)}, )


@login_required(login_url='UserManagement:sign_in')
def task(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        data_class_id = request.POST['data_class_id']
        data_instance_id = request.POST['DataInstanceID']
        task_id = request.POST['task_id']
        print(data_class_id)
        print(data_instance_id)
        print(task_id)
        try:
            with transaction.atomic():
                annotating_data_instance = AnnotationDataSet.objects.get(TaskID=task_id, id=data_instance_id)
                if (annotating_data_instance.WhoIsViewing==user_id) and (annotating_data_instance.IsViewing==True) and (annotating_data_instance.NumberOfAnnotations < Task.objects.get(id=task_id).DataInstanceAnnotationTimes):  # for extra protection.Can be removed if nessasary
                    data_annotation_result = DataAnnotationResult(TaskID=Task.objects.get(id=task_id),
                                                                  DataInstance=annotating_data_instance,
                                                                  ClassID=data_class_id,
                                                                  UserID=user_id)
                    data_annotation_result.save()
                    annotating_data_instance.IsViewing = False
                    annotating_data_instance.WhoIsViewing = 0
                    annotating_data_instance.NumberOfAnnotations += 1
                    annotating_data_instance.save()
                    return redirect('/DoTextDataAnnotationTask/Task?task_id=' + str(task_id))
                else:
                    return HttpResponse('error')
        except DatabaseError:
            return HttpResponse("DatabaseError")
    else:
        try:
            task_id = request.GET['task_id']
            data_instance_annotation_times = int(Task.objects.get(id=task_id).DataInstanceAnnotationTimes)
            print("data_instance_annotation_times")
            annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
            print(1111)
            data_instances_to_exclude = []
            for i in annotated_data_instances:
                data_instances_to_exclude += [i.DataInstance.id]
            try:
                skip_instance=request.GET['skip_instance']
                data_instances_to_exclude += [skip_instance]
                skip_instance_request =True
            except:
                skip_instance_request =False
            print('data_instances_to_exclude')
            try:
                with transaction.atomic():
                    data_annotation = AnnotationDataSet.objects.filter(TaskID=task_id,IsViewing=False,NumberOfAnnotations__lt=data_instance_annotation_times).exclude(id__in=data_instances_to_exclude)
                    print(2)
                    if len(data_annotation) > 0:
                        data_instance = random.choice(data_annotation)
                        print(3)
                        data_instance_about_to_annotate = data_instance #AnnotationDataSet.objects.get(TaskID=task_id, DataInstance=data_instance.DataInstance)
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        sub_data_instances = AnnotationSubDataSet.objects.filter(DataInstanceID=data_instance_about_to_annotate.id)
                        print(4)
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'sub_data_instances':sub_data_instances,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'sub_data_instances': sub_data_instances,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    elif len(data_annotation)==0 and skip_instance_request:
                        data_instance = skip_instance
                        data_instance_about_to_annotate = AnnotationDataSet.objects.get(TaskID=task_id, DataInstance=data_instance.DataInstance)
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        sub_data_instances = AnnotationSubDataSet.objects.filter(DataInstanceID=data_instance_about_to_annotate.id)
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'sub_data_instances': sub_data_instances,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': DataClass.objects.filter(TaskID=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'sub_data_instances': sub_data_instances,
                                                                                                    #'user_id': user_id,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    else:
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoTextDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False,})
            except DatabaseError:
                return HttpResponse("DatabaseError")
        except:
            return redirect('/DoTextDataAnnotationTask/')

@login_required(login_url='UserManagement:sign_in')
def skip_data_instance(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                annotating_data_instance = AnnotationDataSet.objects.get(TaskID=task_id,id=viewing_data_instance)
                if (annotating_data_instance.WhoIsViewing == user_id) and (annotating_data_instance.IsViewing == True):
                    annotating_data_instance.IsViewing = False
                    annotating_data_instance.WhoIsViewing = 0
                    annotating_data_instance.save()
                    return redirect('/DoTextDataAnnotationTask/Task?skip_instance='+viewing_data_instance+'&task_id=' + str(task_id))
                else:
                    return HttpResponse('error')
        except DatabaseError:
            return HttpResponse("DatabaseError")
    except:
        return redirect('/DoTextDataAnnotationTask/Task?task_id=' + str(task_id))

@login_required(login_url='UserManagement:sign_in')
def stop_annotating(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        if stop_viewing(request,task_id,viewing_data_instance):
            return redirect('/DoTextDataAnnotationTask/')
        else:
            return HttpResponse('error')
    except:
        return redirect('/DoTextDataAnnotationTask/')

@login_required(login_url='UserManagement:sign_in')
def stop_viewing(request,task_id,viewing_data_instance):
    try:
        task_id = task_id
        viewing_data_instance = viewing_data_instance
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                annotating_data_instance = AnnotationDataSet.objects.get(TaskID=task_id,id=viewing_data_instance)
                annotating_data_instance.IsViewing = False
                annotating_data_instance.WhoIsViewing = 0
                annotating_data_instance.save()
                return True
        except DatabaseError:
            return False
    except:
        return False


@login_required(login_url='UserManagement:sign_in')
def view_my_annotations(request):
    try:
        task_id = request.GET['task_id']
        user_id = request.session['user_id']
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
        if len(annotated_data_instances) > 0:
            return render(request, 'DoTextDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': True,
                                                               'task_object': Task.objects.get(id=task_id),
                                                               'annotated_data_instances':annotated_data_instances},)
        else:
            return render(request, 'DoTextDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': False,
                                                               'task_object': Task.objects.get(id=task_id), })
    except:
        return redirect('/DoTextDataAnnotationTask/')

@login_required(login_url='UserManagement:sign_in')
def view_my_annotations_change(request):
    if request.method == 'POST':
        annotated_data_instance_id = request.POST['annotated_data_instance_id']
        data_class_id = request.POST['data_class_id']
        data_annotation_result_not_updated = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = data_annotation_result_not_updated.TaskID_id
        data_annotation_result_not_updated.ClassID = data_class_id
        data_annotation_result_not_updated.save()
        return redirect('/DoTextDataAnnotationTask/ViewMyAnnotations?task_id=' + str(task_id))
    else:
        annotated_data_instance_id = request.GET['annotated_data_instance_id']
        #print(annotated_data_instance_id)
        annotated_data_instance = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = annotated_data_instance.TaskID_id
        #print(1234)
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        data_instance = AnnotationDataSet.objects.get(TaskID= task_id ,id = annotated_data_instance.DataInstance.id)
        print(AnnotationSubDataSet.objects.filter(DataInstanceID=data_instance)[0].DataInstance)
        return render(request, 'DoTextDataAnnotationTask/ViewMyAnnotationsChange.html',{'annotated_data_instance':annotated_data_instance,
                                                                                        'annotated_data_instance_id':annotated_data_instance_id,
                                                                                        'data_instance':data_instance,
                                                                                        'sub_data_instances':AnnotationSubDataSet.objects.filter(DataInstanceID=data_instance),
                                                                                        'task_object': Task.objects.get(id=task_id),
                                                                                        'data_classes': DataClass.objects.filter(TaskID=task_id),})
    #return HttpResponse("xasxdsadas")

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
