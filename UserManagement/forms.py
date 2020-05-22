from django_countries.data import COUNTRIES
from django import forms
from . import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    field_choices = [
        ('Engineering', 'Engineering'),
        ('Medicine', 'Medicine'),
        ('Psychology', 'Psychology'),
        ('Art and Culture', 'Art and Culture')
    ]
    email=forms.EmailField(widget=forms.EmailInput())
    confirm_email=forms.EmailField(widget=forms.EmailInput())
    bio = forms.Textarea()
    field = forms.CharField(label="Select your specialized field",
                            widget=forms.Select(choices=field_choices))
    country=forms.ChoiceField(choices = sorted(COUNTRIES.items()))

    class Meta:
        model = models.Profile
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

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        bio = cleaned_data.get("bio")

        if email != confirm_email:
            raise forms.ValidationError(
                "Emails must match!"
            )

        if len(bio) < 10:
            raise forms.ValidationError(
                "Bio must be 10 characters or longer!"
            )

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
