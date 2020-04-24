from django.urls import path
from . import views

urlpatterns = [
    path('', views.first),
    path('test', views.test),
    path('Task', views.task),
    path('ViewMyGenerations',views.view_my_generations),
    path('ViewMyGenerations/Change', views.view_my_generations_change),
    #path('ViewMyGenerations/Delete', views.view_my_generations_delete),
]