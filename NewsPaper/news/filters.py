from django_filters import FilterSet, DateFromToRangeFilter
from .models import Post


class NewsFilter(FilterSet):
    # по диапазону дат
    creation_date = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = {
            # по названию статьи
            'title': ['icontains'],
            # по автору
            'author__user__username': ['icontains'],
        }
