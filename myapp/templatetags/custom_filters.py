# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace_underscore(value):
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value

@register.filter
def replace_space(value):
    if isinstance(value, str):
        return value.replace(' ', '')
    return value

@register.filter
def replace_underscore_no_space(value):
    if isinstance(value, str):
        return value.replace('_', '')
    return value

