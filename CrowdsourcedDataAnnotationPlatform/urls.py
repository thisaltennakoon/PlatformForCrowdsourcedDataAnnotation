from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('UserManagement/', include('UserManagement.urls', namespace='accounts')),
    path('', views.home, name='home'),
]

urlpatterns += staticfiles_urlpatterns()
