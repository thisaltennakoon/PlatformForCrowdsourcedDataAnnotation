from django.contrib import admin
from django.conf.urls import include,url
# from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^task/', include('createtask.urls'))
]
