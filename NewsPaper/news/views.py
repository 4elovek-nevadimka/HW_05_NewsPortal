from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import NewsFilter
from .forms import PostForm
from .models import Post, Category, PostCategory


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10


class FilteredNewsList(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs), 'filter': self.get_filter(),
        }


# дженерик для получения деталей про новость / статью
class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта.
class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm


# дженерик для редактирования объекта.
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_update.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        return Post.objects.get(pk=self.kwargs.get('pk'))


# дженерик для удаления новости / статьи
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AccountView(LoginRequiredMixin, ListView):
    template_name = 'user_account.html'
    model = Category
    context_object_name = 'categories'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# дженерик для получения деталей категории
class CategoryDetailView(DetailView):
    template_name = 'category_detail.html'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_links'] = PostCategory.objects.all()
        return context


@login_required
def subscribe_me(request, cat_id):
    Category.objects.get(pk=cat_id).subscribers.add(request.user)
    return redirect(f'/news/categories/{cat_id}/')


@login_required
def unsubscribe_me(request, cat_id):
    Category.objects.get(pk=cat_id).subscribers.remove(request.user)
    return redirect(f'/news/categories/{cat_id}/')
