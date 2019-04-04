from django import template

register = template.Library()

@register.filter
def current_value(obj):
    return obj.current_value()