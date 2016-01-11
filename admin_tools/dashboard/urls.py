from django.conf.urls import url
from admin_tools.dashboard import views

urlpatterns = [
    url(
        r'^set_preferences/(?P<dashboard_id>.+)/$',
        views.set_preferences,
        name='admin-tools-dashboard-set-preferences'
    ),
]
