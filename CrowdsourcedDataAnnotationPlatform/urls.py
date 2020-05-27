from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('UserManagement/', include('UserManagement.urls', namespace='accounts')),
    path('', views.home, name='home'),
    path('', include('django.contrib.auth.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
