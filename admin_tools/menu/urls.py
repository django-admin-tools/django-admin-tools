from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('admin_tools.menu.views',
    url(r'^add_bookmark/$', 'add_bookmark', name='admin-tools-menu-add-bookmark'),
    url(r'^edit_bookmark/(?P<id>.+)/$', 'edit_bookmark', name='admin-tools-menu-edit-bookmark'),
    url(r'^remove_bookmark/(?P<id>.+)/$', 'remove_bookmark', name='admin-tools-menu-remove-bookmark'),
)
