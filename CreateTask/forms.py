from django import forms
from .models import Cateogary, DescrptiveQuestion, McqQuestion, McqOption, Task
from django.forms import formset_factory, modelformset_factory

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
                # 'placeholder': 'Enter Author Name here'
            }
        )
    }
)


# TextCateogaryFormSet = modelformset_factory(
#     TextCateogary,
#     fields=('cateogaryName',),
#     extra=1,
#     widgets={
#         'cateogaryName': forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Author Name here'
#             }
#         )
#     }
# )


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'instructions', 'field')
        labels = {'title': 'Title', 'description': 'Description', 'instructions': 'Instructions', 'field':'Field'}
        field_choices = [
        ('Engineering', 'Engineering'),
        ('Medicine', 'Medicine'),
        ('Psychology', 'Psychology'),
        ('Art and Culture', 'Art and Culture')
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter Book Name here'
            }
            ),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px',
                # 'placeholder': 'Enter Book Name here'
            }
            ),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px',
                # 'placeholder': 'Enter Book Name here'
            }
            ),
            'field': forms.Select(attrs = {
                'class': 'form-control',
                'style': 'height: 100px',
            })
        }


# class ImageFolderForm(forms.Form):
#     images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


# class CreateTextTaskForm(forms.ModelForm):
#     class Meta:
#         model = TextAnnotationTask
#         fields = ('title', 'description', 'instructions',)
#         labels = {'title':'Title', 'description':'Description', 'instructions':'Instructions'}
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             ),

#             'description': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'style':'height: 100px',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             ),

#             'instructions': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'style':'height: 100px',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             ),

#             #'csvFile': forms.FileField(required=True),
#         }

class CsvForm(forms.Form):
    data = forms.FileField(required=True)


DQuestionFormSet = modelformset_factory(
    DescrptiveQuestion,
    fields=('description',),
    extra=1,
    widgets={
        'Question': forms.TextInput(
            attrs={
                'class': 'form-control',
                # 'placeholder': 'Enter Author Name here'
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

# class zipFile(forms.Form):
#     file = forms.FileField()

# class DataSetForm(forms.Form):
#     file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# class ExampleImagesForm(forms.Form):
#     image_filed = forms.FileField()

# class CreateGenerationTaskForm(forms.ModelForm):
#     class Meta:
#         model = GenerationTask
#         fields = ('title', 'description', 'instructions',)
#         labels = {'title':'Title', 'description':'Description', 'instructions':'Instructions'}
#         widgets = {
#             'title': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             ),

#             'description': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'style':'height: 100px',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             ),

#             'instructions': forms.Textarea(attrs={
#                 'class': 'form-control',
#                 'style':'height: 100px',
#                 #'placeholder': 'Enter Book Name here'
#                 }
#             )
#         }
DATA_CHOICES = [
    ('T', 'Text'),
    ('I', 'Images'),
]


class CustomForm1(forms.Form):
    dataType = forms.ChoiceField(choices=DATA_CHOICES, required=True, label="Data Type need to generate")

# GenerationClassFormSet = modelformset_factory(
#     GenerationClass,
#     fields=('classtitle',),
#     extra=1,
#     widgets={
#         'classtitle': forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#                 #'placeholder': 'Enter Author Name here'
#             }
#         ),
#     }
# )

