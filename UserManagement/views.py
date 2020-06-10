from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,PasswordChangeForm)
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import *
from.filters import ProfileFilter
from .forms import ProfileForm # RateForm
from .models import Profile, ContributorTask
from django.contrib import messages
from CreateTask.models import Task
from .decorators import unauthenticated_user, allowed_user


def sign_in(request):
    if request.user.is_authenticated:
        messages.success(request, 'Please sign out first to sign in with different account')
        return redirect('home')
    else:
        form = SigInForm()
        username = 'not logged in'
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                if form.user_cache is not None:
                    user = form.user_cache
                    username = form.cleaned_data['username']
                    request.session['user_id'] = user.id
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(
                            reverse('home')  # TODO: go to profile
                        )
                    else:
                        messages.error(
                            request,
                            "That user account has been disabled."
                        )
                else:
                    messages.error(
                        request,
                        "Username or password is incorrect."
                    )
        return render(request, 'UserManagement/sign_in.html', {'form': form})

def formView(request):
   if request.session.has_key('username'):
      username = request.session['username']
      return render(request, 'profile.html', {"username" : username})
   else:
      return render(request, 'sign_in.html', {})

def sign_up(request):
    if request.user.is_authenticated:
        messages.success(request, 'Please sign out first to sign up with different account')
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(data=request.POST)
            if form.is_valid():
                new_user = form.save()
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1']
                )
                group = Group.objects.get(name='crowd_user')
                new_user.groups.add(group)
                login(request, user)
                request.session['user_id'] = user.id
                messages.success(request,"Congradulations! Your account was created successfully")
                return HttpResponseRedirect(reverse('UserManagement:edit_profile'))  # TODO: go to profile
        return render(request, 'UserManagement/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    try:
        del request.session['username']
    except:
        pass
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required (login_url='UserManagement:sign_in')
def profile(request):
    """Display User Profile"""
    profile = request.user.profile
    all_user_tasks = ContributorTask.objects.filter(User_id=request.session['user_id'])
    user = request.user
    all_author_tasks = Task.objects.filter(creatorID=user)
    user_text_data_generation_tasks = []
    user_image_data_generation_tasks = []
    user_text_data_annotation_tasks = []
    user_image_data_annotation_tasks = []
    for user_task in all_user_tasks:
        if user_task.Task.taskType == 'TextAnno':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_text_data_annotation_tasks += [user_task.Task]
            else:
                user_text_data_annotation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'ImageAnno':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_image_data_annotation_tasks += [user_task.Task]
            else:
                user_image_data_annotation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'TextGen':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_text_data_generation_tasks += [user_task.Task]
            else:
                user_text_data_generation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'ImgGen':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_image_data_generation_tasks += [user_task.Task]
            else:
                user_image_data_generation_tasks += [user_task.Task]
    return render(request, 'UserManagement/profile.html', {'profile': profile,'all_author_tasks':all_author_tasks, 
                                                        'user_text_data_annotation_tasks': user_text_data_annotation_tasks,
                                                        'user_image_data_annotation_tasks':user_image_data_annotation_tasks,
                                                        'user_text_data_generation_tasks': user_text_data_generation_tasks,
                                                        'user_image_data_generation_tasks': user_image_data_generation_tasks,
                                                        'user_id':request.session['user_id']})


@login_required(login_url='UserManagement:sign_in')
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(models.Profile, user=user)
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile  )
        if form.is_valid():
            form.save()
            messages.success(request, "Updated the Profile Successfully!")
            return HttpResponseRedirect(reverse('UserManagement:profile'))

    return render(request, 'UserManagement/edit_profile.html', {
        'form': form
    })


@login_required(login_url='UserManagement:sign_in')
def change_password(request):
    if request.method == 'POST':
        form = PWChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('UserManagement:profile'))
    else:
        form = PWChangeForm(request.user)
    return render(request, 'UserManagement/change_password.html', {
        'form': form
    })


def search (request):
    profile_list = Profile.objects.all().exclude(first_name = '')
    searchFilter = ProfileFilter(request.GET, queryset=profile_list)
    return render(request, 'UserManagement/search.html', {'filter':searchFilter})

def profiles(request):
    profiles = Profile.objects.all().exclude(first_name = '')
    return render(request,'UserManagement/profile_list.html', {'profiles':profiles})


def view_profile(request, pk):
    profile = Profile.objects.get(user=pk)
    context = {'profile': profile}
    return render(request, 'UserManagement/view_profile.html',context)

@login_required(login_url='UserManagement:sign_in')
@allowed_user(allowed_roles=['admin'])
def delete_profile(request, pk):
    profile = get_object_or_404(Profile, user=pk)
    user = get_object_or_404(User, id=pk)
    context = {'profile': profile}
    if request.method == "POST":
        profile.delete()
        user.delete()
        messages.success(request, 'You have deleted a user')
        return HttpResponseRedirect(reverse('UserManagement:profile_list'))
    return render(request, 'UserManagement/delete_profile.html', context)

@login_required(login_url='UserManagement:sign_in')
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == "POST" :
        task.delete()
        messages.success(request, 'You have deleted a task')
        return HttpResponseRedirect(reverse('UserManagement:author_task_list'))
    return render (request, 'UserManagement/delete_task.html', {'task':task})

"""def rate(request):
    if request.method == "POST":
        form = RateForm()
        if form.is_valid():
            rate = form.save()"""


@login_required(login_url='UserManagement:sign_in')
def view_field_task_list(request):
    user = request.session['user_id']
    profile = Profile.objects.get(user_id=user)
    user_field = profile.field
    registeredTasks = ContributorTask.objects.filter(User_id=user)
    registeredTaskID = []
    for i in registeredTasks:
        registeredTaskID += [i.Task_id]
    all_field_tasks = Task.objects.filter(field=user_field).exclude(creatorID=user)
    all_field_tasks_unregistered = all_field_tasks.exclude(id__in = registeredTaskID)
    #print(all_field_tasks)
    return render (request, 'UserManagement/field_task_list.html', {'all_field_tasks_unregistered':all_field_tasks_unregistered})

@login_required(login_url='UserManagement:sign_in')
def reg_task (request, pk):
    ct = ContributorTask()
    task = get_object_or_404(Task, id=pk)
    user = request.user
    context = {'task':task}
    if request.method=="POST":
        ct.Task=task
        ct.User=user
        ct.save()
        messages.success(request, "You have successfully registered as a contributor")
        return HttpResponseRedirect(reverse('UserManagement:field_task_list'))
    return render(request, 'UserManagement/reg_task.html')

@login_required(login_url='UserManagement:sign_in')
def view_my_tasks(request):
    all_user_tasks = ContributorTask.objects.filter(User_id=request.session['user_id'])
    user_text_data_generation_tasks = []
    user_image_data_generation_tasks = []
    user_text_data_annotation_tasks = []
    user_image_data_annotation_tasks = []
    for user_task in all_user_tasks:
        if user_task.Task.taskType == 'TextAnno':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_text_data_annotation_tasks += [user_task.Task]
            else:
                user_text_data_annotation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'ImageAnno':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_image_data_annotation_tasks += [user_task.Task]
            else:
                user_image_data_annotation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'TextGen':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_text_data_generation_tasks += [user_task.Task]
            else:
                user_text_data_generation_tasks += [user_task.Task]
        elif user_task.Task.taskType == 'ImgGen':
            if len(user_task.Task.description)>140:
                user_task.Task.description1=user_task.Task.description[0:140]
                user_task.Task.description2 = user_task.Task.description[140:]
                user_image_data_generation_tasks += [user_task.Task]
            else:
                user_image_data_generation_tasks += [user_task.Task]
    return render(request, 'UserManagement/MyTasks.html',{'user_text_data_annotation_tasks': user_text_data_annotation_tasks,
                                                          'user_image_data_annotation_tasks':user_image_data_annotation_tasks,
                                                          'user_text_data_generation_tasks': user_text_data_generation_tasks,
                                                          'user_image_data_generation_tasks': user_image_data_generation_tasks,
                                                          'user_id':request.session['user_id']})
@login_required(login_url='UserManagement:sign_in')
def view_author_task(request):
    user = request.session['user_id']
    all_author_tasks = Task.objects.filter(creatorID=user)
    return render (request, 'UserManagement/author_task_list.html', {'all_author_tasks':all_author_tasks})
