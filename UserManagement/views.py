from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       PasswordChangeForm)
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from . import forms
from .models import ContributorTask
from CreateDataGenerationTask.models import Task as DataGenerationTask
from CreateDataAnnotationTask.models import Task as DataAnnotationTask

def sign_in(request):
    form = AuthenticationForm()
    username= 'not logged in'
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form. user_cache is not None:
                user = form.user_cache
                username = form.cleaned_data['username']
                request.session['username'] = username
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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))  # TODO: go to profile
    return render(request, 'UserManagement/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    try:
        del request.session['username']
    except:
        pass
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required(login_url='UserManagement:sign_in')
def profile(request):
    """Display User Profile"""
    profile = request.user.profile

    return render(request, 'UserManagement/profile.html', {
        'profile': profile,
    })


@login_required(login_url='UserManagement:sign_in')
def edit_profile(request):
    user = request.user
    profile = get_object_or_404(models.Profile, user=user)
    form = forms.ProfileForm(instance=profile)

    if request.method == 'POST':
        form = forms.ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated the Profile Successfully!")
            return HttpResponseRedirect(reverse('accounts:profile'))

    return render(request, 'UserManagement/edit_profile.html', {
        'form': form
    })


@login_required(login_url='UserManagement:sign_in')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('UserManagement:profile'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'UserManagement/change_password.html', {
        'form': form
    })

@login_required(login_url='UserManagement:sign_in')
def view_my_tasks(request):
    all_user_tasks = ContributorTask.objects.filter(User_id=request.session['user_id'])
    user_data_generation_tasks = []
    user_data_annotation_tasks = []
    for user_task in all_user_tasks:
        if user_task.Task.taskType=='TextAnno' or user_task.Task.taskType=='ImageAnno':
            user_data_annotation_tasks += [user_task.Task]
        elif user_task.Task.taskType=='TextGen' or user_task.Task.taskType=='ImgGen':
            user_data_generation_tasks += [user_task.Task]
    return render(request, 'UserManagement/MyTasks.html', {'data_generation_tasks': user_data_generation_tasks,
                                                            'data_annotation_tasks':user_data_annotation_tasks,
                                                            'user_id':request.session['user_id']})



