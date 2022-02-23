from django.forms import ModelForm
from .models import Post


# Создаём модельную форму для Новости / Статьи
class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'category_type', 'title', 'text']
