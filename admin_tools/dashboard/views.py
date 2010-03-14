from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

try:
    from django.views.decorators import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt

from forms import DashboardPreferencesForm
from models import DashboardPreferences


@login_required
@csrf_exempt
def set_preferences(request):
    """
    This view serves and validates a preferences form.
    """
    try:
        preferences = DashboardPreferences.objects.get(user=request.user)
    except DashboardPreferences.DoesNotExist:
        preferences = None
    if request.method == "POST":
        form = DashboardPreferencesForm(
            user=request.user,
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
        form = DashboardPreferencesForm(user=request.user, instance=preferences)
    return direct_to_template(request, 'dashboard/preferences_form.html', {
        'form': form,   
    })


@login_required
@csrf_exempt
def get_preferences(request):
    """
    Returns the dashboard preferences for the current user in json format.
    If no preferences are found, the return value is an empty json object.
    """
    try:
        preferences = DashboardPreferences.objects.get(user=request.user)
        data = preferences.data
    except DashboardPreferences.DoesNotExist:
        data = '{}'
    return HttpResponse(data, mimetype='application/json')

