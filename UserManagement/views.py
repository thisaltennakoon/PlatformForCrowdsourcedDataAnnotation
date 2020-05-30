from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,PasswordChangeForm)
from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .forms import CreateUserForm, SigInForm, PWChangeForm
from.filters import ProfileFilter
from .forms import ProfileForm # RateForm
from .models import Profile
from django.contrib import messages


def sign_in(request):
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
            messages.success(request,"Congradulations! Your account was created successfully")
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


@login_required (login_url='UserManagement:sign_in')
def profile(request):
    """Display User Profile"""
    profile = request.user.profile
    return render(request, 'UserManagement/profile.html', {
        'profile': profile
    })


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

def delete_profile(request, pk):
    profile = get_object_or_404(Profile, user=pk)
    user = get_object_or_404(User, id=pk)
    context = {'profile': profile}
    if request.method == "POST":
        profile.delete()
        user.delete()
        #return redirect('UserManagement/profile_list.html')
    return render(request, 'UserManagement/delete_profile.html', context)

"""def rate(request):
    if request.method == "POST":
        form = RateForm()
        if form.is_valid():
            rate = form.save()"""
