from django.contrib import admin
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
# from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^task/', include('createtask.urls'))
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)