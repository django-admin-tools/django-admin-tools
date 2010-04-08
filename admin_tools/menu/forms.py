import urllib

from django import forms

from admin_tools.menu.models import Bookmark

class BookmarkForm(forms.ModelForm):
    """
    This form allows the user to edit bookmarks. It doesn't show the user field.
    It expects the user to be passed in from the view.
    """

    def __init__(self, user, *args, **kwargs):
        super(BookmarkForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_url(self):
        url = self.cleaned_data['url']
        return urllib.unquote(url)

    def save(self, *args, **kwargs):
        bookmark = super(BookmarkForm, self).save(commit=False, *args, **kwargs)
        bookmark.user = self.user
        bookmark.save()
        return bookmark

    class Meta:
        fields = ('url', 'title')
        model = Bookmark
