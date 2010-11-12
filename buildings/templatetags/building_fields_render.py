from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_field(value, name, additional=None):
    res = ""
    if value:
        esc = conditional_escape
        if additional is None:
            res = "<li>%s: <span>%s</span></li>" % (name, esc(value))
        else:
            res = "<li>%s: <span>%s</span> <span>%s</span></li>" % (name, esc(value), additional)
    return mark_safe(res)
render_field.needs_autoescape = True

@register.simple_tag
def flag_field(value, text):
    res = ""
    if value:
        res = "<li>%s</li>" % text
    return res

@register.simple_tag
def pic_flag_field(value, src, title="", alt=""):
    res = ""
    if value:
        res = '<img src="%s" title="%s" alt="%s" />' % (src, title, alt)
    return res

@register.simple_tag
def formfield(field, id, label):
    return '<li>%s<label for="%s">%s</label>%s</li>' % (field.errors, id, label, field)

