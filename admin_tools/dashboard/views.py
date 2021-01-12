from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt

from .forms import DashboardPreferencesForm
from .models import DashboardPreferences
from admin_tools.utils import is_xhr


@staff_member_required
@csrf_exempt
def set_preferences(request, dashboard_id):
    """
    This view serves and validates a preferences form.
    """
    try:
        preferences = DashboardPreferences.objects.get(
            user=request.user, dashboard_id=dashboard_id
        )
    except DashboardPreferences.DoesNotExist:
        preferences = None
    if request.method == "POST":
        form = DashboardPreferencesForm(
            user=request.user,
            dashboard_id=dashboard_id,
            data=request.POST,
            instance=preferences,
        )
        if form.is_valid():
            preferences = form.save()
            if is_xhr(request):
                return HttpResponse("true")
            messages.success(request, "Preferences saved")
        elif is_xhr(request):
            return HttpResponse("false")
    else:
        form = DashboardPreferencesForm(
            user=request.user, dashboard_id=dashboard_id, instance=preferences
        )
    return render(
        request,
        "admin_tools/dashboard/preferences_form.html",
        context={"form": form},
    )
