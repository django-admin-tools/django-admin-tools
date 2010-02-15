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

    def save(self, *args, **kwargs):
        bookmark = super(BookmarkForm, self).save(*args, commit=False, **kwargs)
        bookmark.user = self.user
        bookmark.save()
        return bookmark

    class Meta:
        fields = ('url', 'title')
        model = Bookmark
