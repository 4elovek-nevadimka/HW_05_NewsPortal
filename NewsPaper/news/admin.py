from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post)
