from django.shortcuts import render,redirect,reverse
from .models import DataGenerationResult
from django.http import HttpResponse
from CreateDataGenerationTask.models import Task,GenerationDataSet
from .models import DataGenerationResult
from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from UserManagement.models import ContributorTask

def test(request):
    return render(request, 'DoDataGenerationTask/test.html' )

@login_required(login_url='UserManagement:sign_in')
def first(request):
    all_user_generation_tasks = ContributorTask.objects.filter(UserID_id=request.session['user_id'],
                                                               is_data_annotation_task=False,
                                                               is_data_generation_task=True)
    user_data_generation_tasks = []
    for generation_task in all_user_generation_tasks:
        user_data_generation_tasks += [generation_task.TaskID]
    return render(request, 'DoDataGenerationTask/MyDataGenerationTasks.html', {'tasks': Task.objects.filter(id__in=user_data_generation_tasks)}, )


@login_required(login_url='UserManagement:sign_in')
def task(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        generated_data = request.POST['generated_data']
        data_instance = request.POST['DataInstance']
        task_id = request.POST['task_id']
        genarating_data_instance = GenerationDataSet.objects.get(TaskID=task_id, DataInstance=data_instance)
        if genarating_data_instance.NumberOfGenerations < Task.objects.get(id=task_id).DataInstanceGenerationTimes:  #for extra protection.Can be removed if nessasary
            data_generation_result = DataGenerationResult(TaskID=Task.objects.get(id=task_id),
                                                        DataInstance=data_instance,
                                                        GenerationResult=generated_data,
                                                        UserID=user_id)
            data_generation_result.save()
            genarating_data_instance.NumberOfGenerations += 1
            genarating_data_instance.save()
            return redirect('/DoDataGenerationTask/Task?task_id=' + str(task_id))
        else:
            return HttpResponse('error')
    else:
        try:
            task_id = request.GET['task_id']
            data_instance_generation_times = int(Task.objects.get(id=task_id).DataInstanceGenerationTimes)
            generated_data_instances = DataGenerationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
            data_instances_to_exclude = []
            for i in generated_data_instances:
                data_instances_to_exclude += [i.DataInstance]
            data_generation = GenerationDataSet.objects.filter(TaskID=task_id,NumberOfGenerations__lt=data_instance_generation_times).exclude(DataInstance__in=data_instances_to_exclude)
            if len(data_generation) > 0:
                data_instance = random.choice(data_generation)
                if len(generated_data_instances) > 0:
                    return render(request, 'DoDataGenerationTask/DataGenerationTask.html', {'data_instance_available': True,
                                                                                            'task_object': Task.objects.get(id=task_id),
                                                                                            'data_instance': data_instance,
                                                                                            #'user_id': user_id,
                                                                                            'task_id': task_id,
                                                                                            'generated_data_instances_available': True,
                                                                                            'generated_data_instances': generated_data_instances})
                else:
                    return render(request, 'DoDataGenerationTask/DataGenerationTask.html', {'data_instance_available': True,
                                                                                        'task_object': Task.objects.get(id=task_id),
                                                                                        'data_instance': data_instance,
                                                                                        #'user_id': user_id,
                                                                                        'task_id': task_id,
                                                                                        'generated_data_instances_available': False,})
            else:
                if len(generated_data_instances) > 0:
                    return render(request, 'DoDataGenerationTask/DataGenerationTask.html', {'data_instance_available': False,
                                                                                        'task_object': Task.objects.get(id=task_id),
                                                                                        'task_id': task_id,
                                                                                        'generated_data_instances_available': True,
                                                                                        'generated_data_instances': generated_data_instances})
                else:
                    return render(request, 'DoDataGenerationTask/DataGenerationTask.html', {'data_instance_available': False,
                                                                                        'task_object': Task.objects.get(id=task_id),
                                                                                        'task_id': task_id,
                                                                                        'generated_data_instances_available': False,})
        except:
            return redirect('/DoDataGenerationTask/')


@login_required(login_url='UserManagement:sign_in')
def view_my_generations(request):
    try:
        task_id = request.GET['task_id']
        user_id = request.session['user_id']
        generated_data_instances = DataGenerationResult.objects.filter(TaskID_id=task_id, UserID=user_id).order_by('-LastUpdate')
        if len(generated_data_instances) > 0:
            return render(request, 'DoDataGenerationTask/ViewMyGeneratations.html', {'generated_data_instances_available': True,
                                                               'task_object': Task.objects.get(id=task_id),
                                                               'generated_data_instances':generated_data_instances},)
        else:
            return render(request, 'DoDataGenerationTask/ViewMyGeneratations.html', {'generated_data_instances_available': False,
                                                               'task_object': Task.objects.get(id=task_id), })
    except:
        return redirect('/DoDataGenerationTask/')


@login_required(login_url='UserManagement:sign_in')
def view_my_generations_change(request):
    if request.method == 'POST':
        generated_data_instance_id = request.POST['generated_data_instance_id']
        modification_of_generated_data = request.POST['modification_of_generated_data']
        data_generation_result_not_updated = DataGenerationResult.objects.get(id=generated_data_instance_id)
        task_id = data_generation_result_not_updated.TaskID_id
        data_generation_result_not_updated.GenerationResult = modification_of_generated_data
        data_generation_result_not_updated.save()
        return redirect('/DoDataGenerationTask/ViewMyGenerations?task_id=' + str(task_id))
    else:
        generated_data_instance_id = request.GET['generated_data_instance_id']
        generated_data_instance = DataGenerationResult.objects.get(id=generated_data_instance_id)
        task_id = generated_data_instance.TaskID_id
        return render(request, 'DoDataGenerationTask/ViewMyGenerationsChange.html',{'generated_data_instance':generated_data_instance,
                                                               'task_object': Task.objects.get(id=task_id),})


"""def view_my_generations_delete(request):
    generated_data_instance_id = request.GET['generated_data_instance_id']
    task_id = DataGenerationResult.objects.get(id=generated_data_instance_id).TaskID_id
    try:
        last_confirmation = request.GET['last_confirmation']
        if last_confirmation=="True":

            DataGenerationResult.objects.get(id=generated_data_instance_id).delete()
            return redirect('/DoDataGenerationTask/ViewMyGenerations?task_id='+str(task_id))
        else:
            return redirect('/DoDataGenerationTask/ViewMyGenerations/Change?generated_data_instance_id=' + str(generated_data_instance_id))

    except:
        return render(request, 'DoDataGenerationTask/ViewMyGenerationsDelete.html', {'generated_data_instance_id': generated_data_instance_id,
                                                                                     'task_object':Task.objects.get(id=task_id)})"""

