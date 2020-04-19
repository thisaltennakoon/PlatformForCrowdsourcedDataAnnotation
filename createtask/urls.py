from django.conf.urls import url
from . import views

app_name = 'createtask'

urlpatterns = [

    url(r'^$',views.TaskView.as_view(),name='task_list'),
    url(r'^create/$',views.createTask, name='Anno_task_add'),
    url(r'^new/$', views.test, name= 'test'),
    url(r'^create/addquestion$',views.AddQuestions, name='question_add'),
    url(r'^questionaire/(?P<task_id>[0-9]+)/$',views.QuestionaireView, name='question_view')
]