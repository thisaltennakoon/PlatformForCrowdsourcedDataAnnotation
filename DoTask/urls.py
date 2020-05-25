from django.urls import path
from . import views

urlpatterns = [
    #path('', views.first),
    path('test', views.test),
    path('Task', views.task),
    path('ViewMyContributions',views.view_my_contributions),
    path('ViewMyContributions/Change', views.view_my_contributions_change),
    path('SkipDataInstance', views.skip_data_instance),
    path('StopContributing', views.stop_contributing),
    #path('ViewMyAnnotations/Delete', views.view_my_annotations_delete),
]