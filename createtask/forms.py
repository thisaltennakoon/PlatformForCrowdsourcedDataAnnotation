from django import forms
from .models import AnnotationTask

class CreateTask(forms.ModelForm):
    
    class Meta:
        model = AnnotationTask
        fields = ['title', 'description', 'instructions']