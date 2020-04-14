from django.urls import path
from . import views

urlpatterns = [
    path('', views.first),
    path('Task', views.task),
    path('Task1', views.task1),
]