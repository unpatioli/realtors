from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_field(value, name, safe = False):
    res = ""
    if value:
        if safe != "safe":
            esc = conditional_escape
            value = esc(value)
        res = "<li>%s: <span>%s</span></li>" % (name, value)
    return mark_safe(res)
render_field.needs_autoescape = True

@register.simple_tag
def flag_field(value, text):
    res = ""
    if value:
        res = "<li>%s</li>" % text
    return res
