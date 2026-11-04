try:
    from urllib.parse import unquote, urlparse
except ImportError:
    # Python 2 compatibility
    from urllib import unquote
    from urlparse import urlparse

from django import forms

from admin_tools.menu.models import Bookmark


class BookmarkForm(forms.ModelForm):
    """
    This form allows users to edit bookmarks. It doesn't show the user field.
    It expects the user to be passed in from the view.
    """

    def __init__(self, user, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_url(self):
        url = unquote(self.cleaned_data['url']).strip()
        if urlparse(url).scheme.lower() not in ('', 'http', 'https'):
            raise forms.ValidationError('Invalid URL scheme.')
        return url

    def save(self, *args, **kwargs):
        bookmark = super(BookmarkForm, self).save(
            commit=False,
            *args,
            **kwargs
        )
        bookmark.user = self.user
        bookmark.save()
        return bookmark

    class Meta:
        fields = ('url', 'title')
        model = Bookmark
