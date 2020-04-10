from django.conf.urls import url
from . import views

app_name = 'createtask'

urlpatterns = [

    url(r'^$',views.AnnotationTaskCreate.as_view(), name='Anno_task_add')
]