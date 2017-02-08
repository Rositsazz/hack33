from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def key(dictionary, key):
    # import ipdb; ipdb.set_trace()
    return dictionary[key]
