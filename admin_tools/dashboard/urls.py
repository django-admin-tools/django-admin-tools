from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('admin_tools.dashboard.views',
    url(r'^set_preferences/$', 'set_preferences', name='admin-tools-dashboard-set-preferences'),
)
