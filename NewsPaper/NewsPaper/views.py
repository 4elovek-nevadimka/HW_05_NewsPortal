from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _


# Create your views here.
from django.views import View


class Index(View):
    def get(self, request):
        hello_world = _('Hello world')
        
        context = {
            'hello_world': hello_world
        }
        return HttpResponse(render(request, 'index.html', context))
