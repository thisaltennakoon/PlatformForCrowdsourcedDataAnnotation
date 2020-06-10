from django.urls import path
from . import views

urlpatterns = [
    #path('', views.first),
    #path('test', views.test),
    path('Task', views.task, name='do_text_data_annotation_task'),
    path('ViewMyAnnotations',views.view_my_annotations, name='do_text_data_annotation_view_my_annotations'),
    path('ViewMyAnnotations/Change', views.view_my_annotations_change, name='do_text_data_annotation_view_my_annotations_change'),
    path('SkipDataInstance', views.skip_data_instance, name='do_text_data_annotation_skip_data_instance'),
    path('StopAnnotating', views.stop_annotating, name='do_text_data_annotation_stop_annotating'),
    #path('ViewMyAnnotations/Delete', views.view_my_annotations_delete),
]