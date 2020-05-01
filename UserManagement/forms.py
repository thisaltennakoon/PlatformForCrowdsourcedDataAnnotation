from django_countries.data import COUNTRIES
from django import forms
from . import models

class ProfileForm(forms.ModelForm):
    field_choices = [
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine'),
        ('psychology', 'Psychology'),
        ('art', 'Art and Culture')
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
