from django.urls import path
from . import views

urlpatterns = [
    #path('', views.first),
    path('test', views.test, name='test'),
    path('Task', views.task, name='task'),
    path('ViewMyAnnotations',views.view_my_annotations, name='view_my_annotations'),
    path('ViewMyAnnotations/Change', views.view_my_annotations_change, name='view_my_annotations_change'),
    path('SkipDataInstance', views.skip_data_instance, name='skip_data_instance'),
    path('StopAnnotating', views.stop_annotating, name='stop_annotating'),
    #path('ViewMyAnnotations/Delete', views.view_my_annotations_delete),
]