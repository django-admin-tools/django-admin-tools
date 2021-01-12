import django

if django.VERSION < (2, 0):
    from django.conf.urls import url, include
else:
    from django.urls import re_path as url, include
from admin_tools.menu import views

urlpatterns = [
    url(
        r'^add_bookmark/$',
        views.add_bookmark,
        name='admin-tools-menu-add-bookmark'
    ),
    url(
        r'^edit_bookmark/(?P<id>.+)/$',
        views.edit_bookmark,
        name='admin-tools-menu-edit-bookmark'
    ),
    url(
        r'^remove_bookmark/(?P<id>.+)/$',
        views.remove_bookmark,
        name='admin-tools-menu-remove-bookmark'
    ),
]
