from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Allow dict lookup by variable key in templates: {{ mydict|get_item:key }}"""
    return dictionary.get(key)


@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter: {{ "a,b,c"|split:"," }}"""
    return value.split(delimiter)
