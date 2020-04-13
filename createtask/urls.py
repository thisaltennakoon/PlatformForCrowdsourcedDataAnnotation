from django.conf.urls import url
from . import views

app_name = 'createtask'

urlpatterns = [

    url(r'^create/$',views.createTask, name='Anno_task_add'),
    url(r'^new/$', views.test, name= 'test'),
    url(r'^create/addquestion$',views.AddQuestions, name='question_add')
]