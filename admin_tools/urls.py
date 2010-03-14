from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^menu/', include('admin_tools.menu.urls')),
    url(r'^dashboard/', include('admin_tools.dashboard.urls')),
)
