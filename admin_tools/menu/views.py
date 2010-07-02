from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt

from forms import BookmarkForm
from models import Bookmark


@login_required
@csrf_exempt
def add_bookmark(request):
    """
    This view serves and validates a bookmark form.
    If requested via ajax it also returns the drop bookmark form to replace the 
    add bookmark form.
    """
    if request.method == "POST":
        form = BookmarkForm(user=request.user, data=request.POST)
        if form.is_valid():
            bookmark = form.save()
            if not request.is_ajax():
                request.user.message_set.create(message='Bookmark added')
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponse('Added')
            return direct_to_template(request, 'admin_tools/menu/remove_bookmark_form.html', {
                'bookmark': bookmark,
                'url': bookmark.url,
            });
    else:
        form = BookmarkForm(user=request.user)
    return direct_to_template(request, 'admin_tools/menu/form.html', {
        'form': form,   
        'title': 'Add Bookmark',
    })


@login_required
@csrf_exempt
def edit_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, id=id)
    if request.method == "POST":
        form = BookmarkForm(user=request.user, data=request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            if not request.is_ajax():
                request.user.message_set.create(message='Bookmark updated')
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponse('Saved')
    else:
        form = BookmarkForm(user=request.user, instance=bookmark)
    return direct_to_template(request, 'admin_tools/menu/form.html', {
        'form': form,   
        'title': 'Edit Bookmark',
    })


@login_required
@csrf_exempt
def remove_bookmark(request, id):
    """
    This view deletes a bookmark.
    If requested via ajax it also returns the add bookmark form to replace the 
    drop bookmark form.
    """
    bookmark = get_object_or_404(Bookmark, id=id)
    if request.method == "POST":
        bookmark.delete()
        if not request.is_ajax():
            request.user.message_set.create(message='Bookmark removed')
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST.get('next'))
            return HttpResponse('Deleted')
        return direct_to_template(request, 'admin_tools/menu/add_bookmark_form.html', {
            'url': request.POST.get('next'),
            'title': '**title**' #This gets replaced on the javascript side
        });
    return direct_to_template(request, 'admin_tools/menu/delete_confirm.html', {
        'bookmark': bookmark,
        'title': 'Delete Bookmark',
    })
