from django.views.generic import ListView, DetailView

from .filters import NewsFilter
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-id')
    ordering = ['-id']
    # постраничный вывод
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class FilteredNewsList(ListView):
    model = Post
    template_name = 'filtered_posts.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context
