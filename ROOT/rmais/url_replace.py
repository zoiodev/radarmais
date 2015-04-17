from django import template
from django.template import Library 

register = template.Library()

@register.filter
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()