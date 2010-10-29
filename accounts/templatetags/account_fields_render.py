from django import template

register = template.Library()

@register.simple_tag
def render_field(name, value):
    res = ""
    if value:
        res = "<li>%s: <span>%s</span></li>" % (name, value)
    return res

