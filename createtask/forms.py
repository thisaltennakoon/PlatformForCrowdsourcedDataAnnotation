from django import forms
from .models import AnnotationTask,Cateogary,DescrptiveQuestion,McqQuestion,McqOption
from django.forms import formset_factory,modelformset_factory

# class CreateTaskForm(forms.ModelForm):
    
#     class Meta:
#         model = AnnotationTask
#         fields = ['title', 'description', 'instructions']




CateogaryFormSet = modelformset_factory(
    Cateogary,
    fields=('cateogaryName',),
    extra=1,
    widgets={
        'cateogaryName': forms.TextInput(
            attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Author Name here'
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

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style':'height: 100px',
                #'placeholder': 'Enter Book Name here'
                }
            ),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'style':'height: 100px',
                #'placeholder': 'Enter Book Name here'
                }
            )
        }

DQuestionFormSet = modelformset_factory(
    DescrptiveQuestion,
    fields=('description',),
    extra=1,
    widgets={
        'Question': forms.TextInput(
            attrs={
                'class': 'form-control',
                #'placeholder': 'Enter Author Name here'
            }
        )
    }
)

# McqQuestionFormSet = modelformset_factory(
#     McqQuestion,
#     fields=('description',),
#     extra=1,
#     widgets={
#         'Question': forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Author Name here'
#             }
#         )
#     }
# )

# McqOptionFormSet = modelformset_factory(
#     McqOption,
#     fields=('description',),
#     extra=5,
#     widgets={
#         'Options': forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Author Name here'
#             }
#         )
#     }
# )

class McqForm(forms.Form):
    description = forms.CharField(label="Enter your Question", widget=forms.Textarea)
    correctanswer = forms.CharField(max_length=1000, label="correct answer")
    option1 = forms.CharField(max_length=1000)
    option2 = forms.CharField(max_length=1000)
    option3 = forms.CharField(max_length=1000)
    option4 = forms.CharField(max_length=1000)

McqFormSet = formset_factory(
    McqForm,
    extra=1,
)