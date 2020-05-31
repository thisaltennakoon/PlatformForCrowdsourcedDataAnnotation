from django.conf.urls import url
from . import views

app_name = 'createtask'

urlpatterns = [

    url(r'^$',views.TaskView.as_view(),name='task_list'),
    url(r'^createAnno/$',views.createTask, name='Anno_task_add'),
    url(r'^new/$', views.test, name= 'test'),
    url(r'^create/addquestion$',views.AddQuestions, name='question_add'),
    url(r'^questionaire/(?P<task_id>[0-9]+)/$',views.QuestionaireView, name='question_view'),
    #url(r'^create/example',views.upload_file, name='test_view'),
    url(r'^createTextGen/$',views.createTextGenerationTask, name='Gen_Texttask_add'),
    url(r'^createGen/addexample$',views.AddGenExample, name='Gen_example_add'),
    url(r'^createTextAnno/$',views.createTextTask, name='TextAnno_task_add'),
    url(r'^TextAnnoExampleAdd/$',views.AddTextAnnoExamples, name='TextAnno_example_add'),
]