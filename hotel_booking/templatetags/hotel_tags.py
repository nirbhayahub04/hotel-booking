from django import template

register = template.Library()


@register.filter
def split(value, delimiter):
    return value.split(delimiter)


@register.filter
def range_list(value: int):
    return range(1, value + 1)
