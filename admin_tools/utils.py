"""
Admin ui common utilities.
"""

from django.conf import settings
from django.core.urlresolvers import reverse

class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the 
    AppListMenuItem (to honor the DRY concept).
    """
    def _check_perms(self, request, model, model_admin):
        """
        Checks that the current user can view the given model in the admin.
        """
        mod = '%s.%s' % (model.__module__, model.__name__)

        # check that the app is not in the exclude list
        for pattern in self.exclude_list:
            if mod.startswith(pattern):
                return False

        # check that the app is in the app list (if not empty)
        if len(self.include_list):
            found = False
            for pattern in self.include_list:
                if mod.startswith(pattern):
                    found = True
            if not found:
                return False

        # check that the user has module perms
        if not request.user.has_module_perms(model._meta.app_label):
            return False

        # check whether user has any perm for this module
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            return False
        return perms

    def _get_admin_change_url(self, model):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('admin:%s_%s_changelist' % (app_label,
                                                   model.__name__.lower()))

    def _get_admin_add_url(self, model):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('admin:%s_%s_add' % (app_label, model.__name__.lower()))


def get_media_url():
    """
    Returns the django admin tools media URL.
    """
    return getattr(
        settings,
        'ADMIN_TOOLS_MEDIA_URL',
        getattr(settings, 'STATIC_URL', settings.MEDIA_URL)
    ).rstrip('/')
