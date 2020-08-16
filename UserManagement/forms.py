from django_countries.data import COUNTRIES
from django import forms
from . import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile, ContributorTask
from .filters import ProfileFilter


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'email',
            'bio',
            'is_contributor',
            'is_author',
            'field',
            'country',
        ]

    field_choices = [
        ('Engineering', 'Engineering'),
        ('Medicine', 'Medicine'),
        ('Psychology', 'Psychology'),
        ('Art and Culture', 'Art and Culture')
    ]
    avatar = forms.ImageField(label='avatar', required=False, widget=forms.FileInput(attrs={'class':''}))
    first_name = forms.CharField(label='first_name',widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(label='last_name', required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'placeholder': 'email', 'class':'form-control'}))
    bio = forms.CharField(label='about',widget=forms.TextInput(attrs={'placeholder': 'About', 'class': 'form-control'}))
    field = forms.CharField(label="Select your specialized field",widget=forms.Select(choices=field_choices, attrs={'placeholder':'field', 'class':'form-control'}))
    country = forms.CharField (label="country",widget=forms.Select(choices=sorted(COUNTRIES.items()), attrs={'placeholder':'field', 'class':'form-control'}))
    is_author = forms.BooleanField(label='is_author', required=False, widget=forms.CheckboxInput())
    is_contributor = forms.BooleanField(label='is_contributor', required=False, widget=forms.CheckboxInput())

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': 'username', 'class':'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password','class':'form-control'}))
    password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password confirmation','class':'form-control'}))

class SigInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField(label='username', widget=forms.TextInput(attrs={'placeholder': 'username','class':'form-control'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'password','class':'form-control'}))

class PWChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    old_password = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder': 'current password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder': 'new password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'new password confirmation', 'class': 'form-control'}))

class TaskRegForm(forms.ModelForm):
    class Meta:
        model = ContributorTask
        fields = ['User', 'Task']

class ResetPasswordForm (PasswordResetForm):
    email = forms.EmailField(label='username',widget=forms.EmailInput(attrs={'placeholder': 'email address', 'class': 'form-control'}))

class PasswordSetForm (SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    new_password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'new password', 'class': 'form-control'}))
    new_password2 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder': 'new password confirmation', 'class': 'form-control'}))

"""class RateForm (forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['star']"""