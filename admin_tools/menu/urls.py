from django.conf.urls.defaults import *

urlpatterns = patterns('admin_tools.menu.views',
    url(r'^add_bookmark/$', 'add_bookmark', name='add-bookmark'),
    url(r'^edit_bookmark/(?P<id>.+)/$', 'edit_bookmark', name='edit-bookmark'),
    url(r'^remove_bookmark/(?P<id>.+)/$', 'remove_bookmark', name='remove-bookmark'),
)
