"""
Admin ui common utilities.
"""
from fnmatch import fnmatch

import django
from django.conf import settings
from django.contrib import admin
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
try:
    from importlib import import_module
except ImportError:
    # Django < 1.9 and Python < 2.7
    from django.utils.importlib import import_module
import warnings


def is_xhr(request):
    if django.VERSION < (2, 2):
        return request.is_ajax()
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def uniquify(value, seen_values):
    """ Adds value to seen_values set and ensures it is unique """
    id = 1
    new_value = value
    while new_value in seen_values:
        new_value = "%s%s" % (value, id)
        id += 1
    seen_values.add(new_value)
    return new_value


def get_admin_site(context=None, request=None):
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultIndexDashboard'
    )

    if isinstance(dashboard_cls, dict):
        if context:
            request = context.get('request')
        curr_url = request.path
        for key in dashboard_cls:
            mod, inst = key.rsplit('.', 1)
            mod = import_module(mod)
            admin_site = getattr(mod, inst)
            admin_url = reverse('%s:index' % admin_site.name)
            if curr_url.startswith(admin_url):
                return admin_site
    else:
        return admin.site
    raise ValueError('Admin site matching "%s" not found' % dashboard_cls)


def get_admin_site_name(context):
    return get_admin_site(context).name


def get_avail_models(request):
    """ Returns (model, perm,) for all models user can possibly see """
    items = []
    admin_site = get_admin_site(request=request)

    for model, model_admin in admin_site._registry.items():
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            continue
        items.append((model, perms,))
    return items


def filter_models(request, models, exclude):
    """
    Returns (model, perm,) for all models that match models/exclude patterns
    and are visible by current user.
    """
    items = get_avail_models(request)
    included = []

    def full_name(model):
        return '%s.%s' % (model.__module__, model.__name__)

    # I beleive that that implemented
    # O(len(patterns)*len(matched_patterns)*len(all_models))
    # algorythm is fine for model lists because they are small and admin
    # performance is not a bottleneck. If it is not the case then the code
    # should be optimized.

    if len(models) == 0:
        included = items
    else:
        for pattern in models:
            wildcard_models = []
            for item in items:
                model, perms = item
                model_str = full_name(model)
                if model_str == pattern:
                    # exact match
                    included.append(item)
                elif fnmatch(model_str, pattern) and \
                        item not in wildcard_models:
                    # wildcard match, put item in separate list so it can be
                    # sorted alphabetically later
                    wildcard_models.append(item)
            if wildcard_models:
                # sort wildcard matches alphabetically before adding them
                wildcard_models.sort(
                    key=lambda x: x[0]._meta.verbose_name_plural
                )
                included += wildcard_models

    result = included[:]
    for pattern in exclude:
        for item in included:
            model, perms = item
            if fnmatch(full_name(model), pattern):
                try:
                    result.remove(item)
                except ValueError:  # if the item was already removed skip
                    pass
    return result


class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the
    AppListMenuItem (to honor the DRY concept).
    """

    def _visible_models(self, request):
        # compatibility layer: generate models/exclude patterns
        # from include_list/exclude_list args

        if self.include_list:
            warnings.warn(
               "`include_list` is deprecated for ModelList and AppList and "
               "will be removed in future releases. Please use `models` "
               "instead.",
               DeprecationWarning
            )

        if self.exclude_list:
            warnings.warn(
               "`exclude_list` is deprecated for ModelList and AppList and "
               "will be removed in future releases. Please use `exclude` "
               "instead.",
               DeprecationWarning
            )

        included = self.models[:]
        included.extend([elem+"*" for elem in self.include_list])

        excluded = self.exclude[:]
        excluded.extend([elem+"*" for elem in self.exclude_list])
        if self.exclude_list and not included:
            included = ["*"]
        return filter_models(request, included, excluded)

    def _get_admin_app_list_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:app_list' % get_admin_site_name(context),
                       args=(app_label,))

    def _get_admin_change_url(self, model, context):
        """
        Returns the admin change url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_changelist' % (get_admin_site_name(context),
                                                app_label,
                                                model.__name__.lower()))

    def _get_admin_add_url(self, model, context):
        """
        Returns the admin add url.
        """
        app_label = model._meta.app_label
        return reverse('%s:%s_%s_add' % (get_admin_site_name(context),
                                         app_label,
                                         model.__name__.lower()))
