from django import template

register = template.Library()

@register.filter(name='truncate')
def truncate(value, arg):
    if len(value) > arg:
        value = "%s..." % value[0:arg]
    return value

