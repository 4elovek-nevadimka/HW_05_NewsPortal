from django import template
from django.contrib.auth.models import User

register = template.Library()

bad_words = []
with open('bad_words.txt', encoding='utf-8-sig') as input_file:
    # print('bad words loaded')
    for line in input_file:
        if len(line.strip()) > 1:
            bad_words.append(line.strip())


@register.filter(name='censor')
def censor(value):
    if isinstance(value, str):
        for bad_word in bad_words:
            value = value.replace(bad_word, '*' * len(bad_word))
        return value
    else:
        raise ValueError(f'Неверный входной тип данных: {type(value)} должен быть строкой!')


@register.filter(name='subscribed')
def subscribed(qs, user):
    try:
        qs.get(pk=user.id)
        return True
    except User.DoesNotExist:
        return False


@register.filter(name='by_category')
def by_category(post_cat_list, category_id):
    return post_cat_list.filter(category=category_id)
