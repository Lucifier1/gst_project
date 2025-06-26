from django import template

register = template.Library()

@register.filter
def to(value_first,value_second):
    return range(value_second)