from django.conf.urls.defaults import *

urlpatterns = patterns('admin_tools.dashboard.views',
    url(r'^get_preferences/$', 'get_preferences', name='admin-tools-dashboard-get-preferences'),
    url(r'^set_preferences/$', 'set_preferences', name='admin-tools-dashboard-set-preferences'),
)
