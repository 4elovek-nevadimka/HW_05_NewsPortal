from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


@login_required
def downgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        premium_group.user_set.remove(user)
    return redirect('/news/')
