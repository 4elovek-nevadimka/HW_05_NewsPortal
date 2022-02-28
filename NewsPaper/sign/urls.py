from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import upgrade_me

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('downgrade/', upgrade_me, name='downgrade'),
]
