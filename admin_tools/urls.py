from django.conf import settings
from django.conf.urls import url, include

urlpatterns = []
if 'admin_tools.menu' in settings.INSTALLED_APPS:
    urlpatterns.append(url(r'^menu/', include('admin_tools.menu.urls')))
if 'admin_tools.dashboard' in settings.INSTALLED_APPS:
    urlpatterns.append(
        url(r'^dashboard/', include('admin_tools.dashboard.urls'))
    )
