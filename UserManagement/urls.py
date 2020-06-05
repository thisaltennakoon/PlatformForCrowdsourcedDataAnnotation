from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'UserManagement'

urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path ('search/', views.search, name='search'),
    #path ('rate/', views.rate, name='rate'),

    path ('profile_list/', views.profiles, name='profile_list'),
    path ('profile_list/view_profile/<str:pk>', views.view_profile, name='view_profile'),
    path ('profile_list/delete_profile/<str:pk>',views.delete_profile, name="delete_profile"),

    path('reset_password/', auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64/token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('MyTasks/', views.view_my_tasks , name = 'MyTasks'),
    path('Task_list/', views.view_field_task_list, name='field_task_list')

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)



