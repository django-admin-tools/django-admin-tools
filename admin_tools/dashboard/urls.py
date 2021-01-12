import django

if django.VERSION < (2, 0):
    from django.conf.urls import url
else:
    from django.urls import re_path as url

from admin_tools.dashboard import views

urlpatterns = [
    url(
        r'^set_preferences/(?P<dashboard_id>.+)/$',
        views.set_preferences,
        name='admin-tools-dashboard-set-preferences'
    ),
]
