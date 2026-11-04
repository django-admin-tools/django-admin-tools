from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages

from .forms import BookmarkForm
from .models import Bookmark
from admin_tools.utils import get_safe_next_url, is_xhr


@staff_member_required
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
            if not is_xhr(request):
                messages.success(request, "Bookmark added")
                next_url = get_safe_next_url(request)
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponse("Added")
            return render(
                request,
                "admin_tools/menu/remove_bookmark_form.html",
                context={"bookmark": bookmark, "url": bookmark.url},
            )
    else:
        form = BookmarkForm(user=request.user)
    return render(
        request,
        "admin_tools/menu/form.html",
        context={"form": form, "title": "Add Bookmark"},
    )


@staff_member_required
def edit_bookmark(request, id):
    bookmark = get_object_or_404(Bookmark, id=id, user=request.user)
    if request.method == "POST":
        form = BookmarkForm(
            user=request.user, data=request.POST, instance=bookmark
        )
        if form.is_valid():
            form.save()
            if not is_xhr(request):
                messages.success(request, "Bookmark updated")
                next_url = get_safe_next_url(request)
                if next_url:
                    return HttpResponseRedirect(next_url)
            return HttpResponse("Saved")
    else:
        form = BookmarkForm(user=request.user, instance=bookmark)
    return render(
        request,
        "admin_tools/menu/form.html",
        context={"form": form, "title": "Edit Bookmark"},
    )


@staff_member_required
def remove_bookmark(request, id):
    """
    This view deletes a bookmark.
    If requested via ajax it also returns the add bookmark form to replace the
    drop bookmark form.
    """
    bookmark = get_object_or_404(Bookmark, id=id, user=request.user)
    if request.method == "POST":
        bookmark.delete()
        if not is_xhr(request):
            messages.success(request, "Bookmark removed")
            next_url = get_safe_next_url(request)
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponse("Deleted")
        return render(
            request,
            "admin_tools/menu/add_bookmark_form.html",
            context={
                "url": request.POST.get("next"),
                "title": "**title**",  # replaced on the javascript side
            },
        )
    return render(
        request,
        "admin_tools/menu/delete_confirm.html",
        context={"bookmark": bookmark, "title": "Delete Bookmark"},
    )
