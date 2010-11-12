from django import template

register = template.Library()

@register.simple_tag
def formfield(field, label, id=None):
    if id is None:
        id = field.auto_id
    return '<li>%s<label for="%s">%s</label> %s</li>' % (field.errors, id, label, field)

@register.simple_tag
def gtlt_field(gt_field, lt_field, label, id=None):
    if id is None:
        id = gt_field.auto_id
    return '<li>%s %s<label for="%s">%s</label>%s - %s</li>' % (gt_field.errors, lt_field.errors, id, label, gt_field, lt_field)

