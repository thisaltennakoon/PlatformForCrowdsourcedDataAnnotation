from django.urls import path
from . import views

urlpatterns = [
    path('', views.first),
    path('test', views.test),
    path('Task', views.task),
    path('ViewMyAnnotations',views.view_my_annotations),
    path('ViewMyAnnotations/Change', views.view_my_annotations_change),
    path('SkipDataInstance', views.skip_data_instance),
    path('StopAnnotating', views.stop_annotating),
    #path('ViewMyAnnotations/Delete', views.view_my_annotations_delete),
]