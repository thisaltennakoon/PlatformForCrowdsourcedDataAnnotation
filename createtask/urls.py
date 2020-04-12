from django.conf.urls import url
from . import views

app_name = 'createtask'

urlpatterns = [

    url(r'^create/$',views.CreateTaskView.as_view(), name='Anno_task_add'),
    url(r'^new/$', views.createTask)
]