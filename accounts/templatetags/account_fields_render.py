from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_field(name, value):
    res = ""
    if value:
        esc = conditional_escape
        res = "<li>%s: <span>%s</span></li>" % (name, esc(value))
    return mark_safe(res)
render_field.needs_autoescape = True

