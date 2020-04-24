from django.urls import path
from . import views

urlpatterns = [
    path('SignIn/', views.Sign_in, name = 'SignIn' ),
    path('MyTasks/', views.view_my_tasks , name = 'MyTasks'),
]