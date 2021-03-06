from django.urls import path
from .views import NewsList, FilteredNewsList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    AccountView, CategoryDetailView, subscribe_me, unsubscribe_me

urlpatterns = [
    # Просто список новостей / статей
    path('', NewsList.as_view(), name='post_list'),
    # Страница с возможностью фильтрации постов
    path('search/', FilteredNewsList.as_view(), name='post_filter'),
    # Ссылка на конкретную новость / статью
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    # Ссылка на добавление новости / статьи
    path('add/', PostCreateView.as_view(), name='post_add'),
    # Ссылка на редактирование новости / статьи
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    # Ссылка на удаление новости / статьи
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('account/', AccountView.as_view(), name='account'),

    # Ссылка на конкретную категорию
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),

    path('subscribe/<int:cat_id>', subscribe_me, name='subscribe'),
    path('unsubscribe/<int:cat_id>', unsubscribe_me, name='unsubscribe'),
]
