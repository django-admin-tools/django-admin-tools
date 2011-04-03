from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt

from forms import DashboardPreferencesForm
from models import DashboardPreferences


@login_required
@csrf_exempt
def set_preferences(request, dashboard_id):
    """
    This view serves and validates a preferences form.
    """
    try:
        preferences = DashboardPreferences.objects.get(
            user=request.user,
            dashboard_id=dashboard_id
        )
    except DashboardPreferences.DoesNotExist:
        preferences = None
    if request.method == "POST":
        form = DashboardPreferencesForm(
            user=request.user,
            dashboard_id=dashboard_id,
            data=request.POST,
            instance=preferences
        )
        if form.is_valid():
            preferences = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            request.user.message_set.create(message='Preferences saved')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = DashboardPreferencesForm(
            user=request.user,
            dashboard_id=dashboard_id,
            instance=preferences
        )
    return direct_to_template(request, 'admin_tools/dashboard/preferences_form.html', {
        'form': form,   
    })
