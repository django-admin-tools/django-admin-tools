try:
    from django.conf.urls import url, include
except ImportError: # django < 1.4
    from django.conf.urls.defaults import url, include
from django.conf import settings
from django.contrib import admin
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
