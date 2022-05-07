import pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.utils import timezone

from django.views import View


class Index(View):
    def get(self, request):
        hello_world = _('Hello world')

        context = {
            'hello_world': hello_world,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones
        }
        return HttpResponse(render(request, 'index.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
