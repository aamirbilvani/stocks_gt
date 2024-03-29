from django import template

register = template.Library()

@register.filter
def current_value(obj):
    return obj.current_value()

@register.filter
def original_value(obj):
    return obj.original_value()

@register.filter
def daily_pl(obj):
    return obj.daily_pl()

@register.filter
def daily_pl_percent(obj):
    return obj.daily_pl_percent()

@register.filter
def total_pl(obj):
    return obj.total_pl()

@register.filter
def total_pl_percent(obj):
    return obj.total_pl_percent()

@register.filter
def ytd_pl(obj):
    return obj.ytd_pl()

@register.filter
def ytd_pl_percent(obj):
    return obj.ytd_pl_percent()

@register.filter
def annualized_return(obj):
    return obj.annualized_return()

@register.filter
def sign(obj):
    if obj > 0:
        return "positive"
    elif obj < 0:
        return "negative"
    else:
        return "zero"
