import urllib.parse

from django import template
from django.http import QueryDict

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the
    current ones, only with the specified GET parameters changed.
    """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urllib.parse.urlencode(query)
