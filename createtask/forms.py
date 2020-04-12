from django import forms
from .models import AnnotationTask,Cateogary
from django.forms import formset_factory,modelformset_factory

# class CreateTaskForm(forms.ModelForm):
    
#     class Meta:
#         model = AnnotationTask
#         fields = ['title', 'description', 'instructions']

class AddCateogariesForm(forms.Form):
    cateogary = forms.CharField()


CateogaryFormSet = modelformset_factory(
    Cateogary,
    fields=('cateogaryName',),
    extra=1,
    widgets={
        'cateogaryName': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Author Name here'
            }
        )
    }
)

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = AnnotationTask
        fields = ('title', 'description', 'instructions',)
        labels = {'title':'Title', 'description':'Description', 'instructions':'Instructions'}
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Book Name here'
                }
            ),

            'description': forms.TextInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Book Name here'
                }
            ),

            'instructions': forms.TextInput(attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Book Name here'
                }
            )
        }