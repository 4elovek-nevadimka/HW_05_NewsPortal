from django_filters import FilterSet
from .models import Post


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            # по дате
            'creation_date': ['icontains'],
            # по названию статьи
            'title': ['icontains'],
            # по автору
            'author__user__username': ['icontains'],
        }
