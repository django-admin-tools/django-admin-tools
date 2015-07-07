from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items, Menu

# to activate your custom menu add the following to your settings.py:
#
# ADMIN_TOOLS_MENU = 'test_proj.menu.CustomMenu'

class CustomMenu(Menu):
    """
    Custom Menu for test_proj admin site.
    """
    class Media:
        css = {
            'all': ('test_app/menu.css',),
        }
        js = ('test_app/menu.js',)

    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                _('Applications'),
                exclude=('django.contrib.*',)
            ),
            items.AppList(
                _('Administration'),
                models=('django.contrib.*',)
            ),
            items.ModelList(
                'Test app menu',
                ['test_app.models.Bar', 'django.contrib.auth.*']
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
