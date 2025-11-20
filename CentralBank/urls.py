from django.contrib import admin
from django.urls import path as url
from django.conf.urls import include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('admin/', admin.site.urls),
    url('', views.index, name = "home"),
    url('accounts/', include("accounts.urls")),
    url('profile/', include("profiles.urls")),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#Change Site Title, Index Title and Site Title
admin.site.site_header = "Central Bank Administration"
admin.site.site_title = "Central Bank Administration"
admin.site.index_title = "Welcome to Central Bank Administration Admin Panel"
