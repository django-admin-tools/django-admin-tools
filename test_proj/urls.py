import django

if django.VERSION < (2, 0):
    from django.conf.urls import url, include
else:
    from django.urls import re_path as url, include

from django.conf import settings
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
