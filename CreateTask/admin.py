
from django.contrib import admin

from .models import Task,UserNew2,Cateogary,DescrptiveQuestion,Questionaire,McqOption,TextFile,TextDataInstance,TextData,MediaDataInstance,DataGenTextInstance, \
    ExampleTextDataInstance,ExampleTextData,ExampleTextAnnoResult,AnnotationTest,ExampleMediaDataInstance,ExampleMediaAnnoResult,MediaAnnoAnswers


# Register your models here.
admin.site.register(Task)
#admin.site.register(UserNew2)
admin.site.register(Cateogary)
# admin.site.register(DescrptiveQuestion)
# admin.site.register(Questionaire)
# admin.site.register(McqOption)
# admin.site.register(GenerationTask)
# admin.site.register(GenerationClass)
# admin.site.register(TextAnnotationTask)
admin.site.register(TextFile)
admin.site.register(TextDataInstance)
admin.site.register(TextData)
admin.site.register(MediaDataInstance)
admin.site.register(DataGenTextInstance)
admin.site.register(ExampleTextDataInstance)
admin.site.register(ExampleTextData)
admin.site.register(ExampleTextAnnoResult)
admin.site.register(AnnotationTest)
admin.site.register(MediaAnnoAnswers)
admin.site.register(ExampleMediaAnnoResult)
admin.site.register(ExampleMediaDataInstance)

