from django.urls import path
from .views import NewsList, NewsDetail, FilteredNewsList

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view()),
    path('search', FilteredNewsList.as_view()),
]
