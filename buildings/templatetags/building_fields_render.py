from django import template

register = template.Library()

@register.simple_tag
def render_field(name, value, additional=None):
    res = ""
    if value:
        if additional is None:
            res = "<li>%s: <span>%s</span></li>" % (name, value)
        else:
            res = "<li>%s: <span>%s</span> <span>%s</span></li>" % (name, value, additional)
    return res

