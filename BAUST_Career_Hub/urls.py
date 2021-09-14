
from django.conf.urls import url
from . import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.contrib.auth import views

urlpatterns = [
    #path('accounts/', include('Admin_app.urls')),
    path('admin/', admin.site.urls),
    path('', include('Admin_app.urls')),
    path('p/', include('post.urls')),
    path('notification/', include('notification.urls')),
    path('inbox/', include('messanger.urls')),
] 
# urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

