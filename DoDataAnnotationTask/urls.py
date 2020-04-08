from django.urls import path
from . import views

urlpatterns = [
    path('', views.first),
    path('Task', views.task),
]