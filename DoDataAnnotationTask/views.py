from django.shortcuts import render, redirect, reverse
from .models import DataAnnotationResult
from django.http import HttpResponse
from CreateTask.models import Task, Cateogary, MediaDataInstance
from .models import DataAnnotationResult
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from UserManagement.models import ContributorTask,Profile
from django.db import DatabaseError, transaction
import datetime

def test(request):
    return render(request, 'DoDataAnnotationTask/test.html')

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
    if request.method == 'POST': # This part will only execute after submitting annotation answer for given data instance
        data_class_id = request.POST['data_class_id']
        data_instance = request.POST['DataInstance']
        task_id = request.POST['task_id']
        try:
            with transaction.atomic():
                annotating_data_instance = MediaDataInstance.objects.get(taskID_id=task_id, media=data_instance)
                # system will check whether the data instance is belongs to this user for more accuracy.
                if (annotating_data_instance.WhoIsViewing==user_id) and (annotating_data_instance.IsViewing==True) and (annotating_data_instance.NumberOfAnnotations < Task.objects.get(id=task_id).requiredNumofAnnotations):  # for extra protection.Can be removed if nessasary
                    # create data annotation result and save it in the database
                    data_annotation_result = DataAnnotationResult(TaskID=Task.objects.get(id=task_id),
                                                                  DataInstance=annotating_data_instance,
                                                                  ClassID=data_class_id,
                                                                  UserID=user_id)
            
                    data_annotation_result.save()
                    # release the lock for submitted data instance
                    annotating_data_instance.IsViewing = False
                    annotating_data_instance.WhoIsViewing = 0
                    annotating_data_instance.NumberOfAnnotations += 1
                    annotating_data_instance.save()
                    return redirect('/DoDataAnnotationTask/Task?task_id=' + str(task_id))
                else:
                    return redirect('/DoDataAnnotationTask/Task?task_id=' + str(task_id))
        except DatabaseError:
            print('DatabaseError in task() annotation submission Image Data Annotation')
            return redirect('/UserManagement/MyTasks/')
    else: # this part is responsible for giving data instance to annotate. This will execute after clicking a task, submitting an annotation or skipping a data instance
        try:
            task_id = request.GET['task_id']
            if len(ContributorTask.objects.filter(User_id=user_id, Task_id=task_id)) == 0:# check whether this user is registerd for this task
                return redirect('/UserManagement/MyTasks/')
            data_instance_annotation_times = int(Task.objects.get(id=task_id).requiredNumofAnnotations) # Take required number of annotations for the task
            annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')# Take submitted annotation for this task by this user so that we can prevent being annotate same data instance by the same user.
            data_instances_to_exclude = [] # add those data instance to this list
            for i in annotated_data_instances:
                data_instances_to_exclude += [i.DataInstance.id]
            try:# there is an option to skip data instances. here skipped data instances are addded to excluding data instances list so that annotator will not get those data instances.
                skip_instance=request.GET['skip_instance']
                skip_instance_object = MediaDataInstance.objects.get(taskID_id=task_id, media=skip_instance)
                data_instances_to_exclude += [skip_instance_object.id]
                skip_instance_request =True
            except:
                skip_instance_request =False
            try:
                with transaction.atomic():
                    data_annotation = MediaDataInstance.objects.filter(taskID_id=task_id,IsViewing=False,NumberOfAnnotations__lt=data_instance_annotation_times).exclude(id__in=data_instances_to_exclude) 
                    # take data instances which are not viewing and number of annotations are less than required number of annotations while excluding the data instances which have annotated already by this user
                    if len(data_annotation) > 0:
                        data_instance = random.choice(data_annotation) # choose one data instance randomly and put a lock to that data instance before giving.
                        data_instance_about_to_annotate = MediaDataInstance.objects.get(taskID_id=task_id, media=data_instance.media)
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    elif len(data_annotation)==0 and skip_instance_request: # if contributor wants to skip the only remaining data instance, same data instance will be given again and again
                        data_instance = MediaDataInstance.objects.get(taskID_id=task_id, id=skip_instance_object.id)
                        data_instance_about_to_annotate = data_instance
                        data_instance_about_to_annotate.IsViewing=True
                        data_instance_about_to_annotate.WhoIsViewing=user_id
                        data_instance_about_to_annotate.save()
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': True,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                                    'data_instance': data_instance,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'task_id': task_id,
                                                                                                    'annotated_data_instances_available': False})
                    else: # if all the data instances have been annotated, system will automatically change the status of the task as 'completed'
                        remaining_data_instances = MediaDataInstance.objects.filter(taskID_id=task_id,NumberOfAnnotations__lt=data_instance_annotation_times)
                        if len(remaining_data_instances)==0:
                            completed_task = Task.objects.get(id=task_id)
                            if completed_task.status=='inprogress':
                                completed_task.status = 'completed'
                                completed_task.save()
                        if len(annotated_data_instances) > 0:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'annotated_data_instances_available': True,
                                                                                                    'annotated_data_instances': annotated_data_instances})
                        else:
                            return render(request, 'DoDataAnnotationTask/DataAnnotationTask.html', {'data_instance_available': False,
                                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                                    'task_id': task_id,
                                                                                                    'first_name':Profile.objects.get(user=request.user).first_name,
                                                                                                    'annotated_data_instances_available': False,})
            except DatabaseError:
                print('DatabaseError in task() giving data instance to annotator Image data annotation')
                return redirect('/UserManagement/MyTasks/')
        except:
            print('Failure in task() Image data annotation ')
            return redirect('/UserManagement/MyTasks/')

@login_required(login_url='UserManagement:sign_in')
def skip_data_instance(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                if stop_viewing(request,task_id,viewing_data_instance):
                    print('skip_data_instance1')
                    return redirect('/DoDataAnnotationTask/Task?skip_instance='+viewing_data_instance+'&task_id=' + str(task_id))
                else:
                    return HttpResponse('error')
        except DatabaseError:
            print('DatabaseError in skip_data_instance()  Image data annotation')
            return redirect('/UserManagement/MyTasks/')
    except:
        return redirect('/DoDataAnnotationTask/Task?task_id=' + str(task_id))

@login_required(login_url='UserManagement:sign_in')
def stop_annotating(request):
    try:
        task_id = request.GET['task_id']
        viewing_data_instance = request.GET['viewing_data_instance']
        user_id = request.session['user_id']
        if stop_viewing(request,task_id,viewing_data_instance):
            return redirect('/UserManagement/MyTasks/')
        else:
            print('Error in stop_annotating()  Image data annotation')
            return redirect('/UserManagement/MyTasks/')
    except:
        print('Error in stop_annotating()  Image data annotation')
        return redirect('/UserManagement/MyTasks/')

@login_required(login_url='UserManagement:sign_in')
def stop_viewing(request,task_id,viewing_data_instance):
    try:
        task_id = task_id
        viewing_data_instance = viewing_data_instance
        user_id = request.session['user_id']
        try:
            with transaction.atomic():
                annotating_data_instance = MediaDataInstance.objects.get(taskID_id=task_id,media=viewing_data_instance)
                if (annotating_data_instance.WhoIsViewing == user_id) and (annotating_data_instance.IsViewing == True):
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
        user_id = request.session['user_id']
        task_id = request.GET['task_id']
        if len(ContributorTask.objects.filter(User_id=user_id, Task_id=task_id)) == 0:
            return redirect('/UserManagement/MyTasks/')
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        annotated_data_instances = DataAnnotationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
        if len(annotated_data_instances) > 0:
            return render(request, 'DoDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': True,
                                                               'task_object': Task.objects.get(id=task_id),
                                                               'annotated_data_instances':annotated_data_instances},)
        else:
            return render(request, 'DoDataAnnotationTask/ViewMyAnnotations.html', {'annotated_data_instances_available': False,
                                                               'task_object': Task.objects.get(id=task_id), })
    except:
        print('Error in view_my_annotations()  Image data annotation')
        return redirect('/UserManagement/MyTasks/')

@login_required(login_url='UserManagement:sign_in')
def view_my_annotations_change(request):
    if request.method == 'POST':
        annotated_data_instance_id = request.POST['annotated_data_instance_id']
        data_class_id = request.POST['data_class_id']
        data_annotation_result_not_updated = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = data_annotation_result_not_updated.TaskID_id
        data_annotation_result_not_updated.ClassID = data_class_id
        data_annotation_result_not_updated.save()
        return redirect('/DoDataAnnotationTask/ViewMyAnnotations?task_id=' + str(task_id))
    else:
        annotated_data_instance_id = request.GET['annotated_data_instance_id']
        annotated_data_instance = DataAnnotationResult.objects.get(id=annotated_data_instance_id)
        task_id = annotated_data_instance.TaskID_id
        try:
            viewing_data_instance = request.GET['viewing_data_instance']
            stop_viewing(request, task_id, viewing_data_instance)
        except:
            pass
        data_instance = MediaDataInstance.objects.get(id = annotated_data_instance.DataInstance.id)
        return render(request, 'DoDataAnnotationTask/ViewMyAnnotationsChange.html',{'annotated_data_instance':annotated_data_instance,
                                                                                    'annotated_data_instance_id':annotated_data_instance_id,
                                                                                     'data_instance':data_instance,
                                                                                    'task_object': Task.objects.get(id=task_id),
                                                                                     'data_classes': Cateogary.objects.filter(taskID_id=task_id),
                                                                                    })
