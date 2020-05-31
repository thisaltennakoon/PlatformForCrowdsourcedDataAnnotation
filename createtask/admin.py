from django.contrib import admin
from .models import Task,UserNew2,Cateogary,DescrptiveQuestion,Questionaire,McqOption,TextFile,TextDataInstance,TextData,DataGenTextInstance

# Register your models here.
admin.site.register(Task)
admin.site.register(UserNew2)
admin.site.register(Cateogary)
admin.site.register(DescrptiveQuestion)
admin.site.register(Questionaire)
admin.site.register(McqOption)
# admin.site.register(GenerationTask)
# admin.site.register(GenerationClass)
# admin.site.register(TextAnnotationTask)
admin.site.register(TextFile)
admin.site.register(TextDataInstance)
admin.site.register(TextData)
admin.site.register(DataGenTextInstance)