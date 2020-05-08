from django.contrib import admin
from .models import AnnotationTask,UserNew2,Cateogary,DescrptiveQuestion,Questionaire,McqOption,GenerationTask,GenerationClass,TextAnnotationTask

# Register your models here.
admin.site.register(AnnotationTask)
admin.site.register(UserNew2)
admin.site.register(Cateogary)
admin.site.register(DescrptiveQuestion)
admin.site.register(Questionaire)
admin.site.register(McqOption)
admin.site.register(GenerationTask)
admin.site.register(GenerationClass)
admin.site.register(TextAnnotationTask)