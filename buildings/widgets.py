from django import forms

class DivCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        if 'classes' in kwargs:
            self.classes = kwargs.pop('classes')
        else:
            self.classes = []
        super(DivCheckboxSelectMultiple, self).__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None):
        from django.utils.safestring import mark_safe
        res_super = super(DivCheckboxSelectMultiple, self).render(name, value, attrs=attrs)
        res = mark_safe(u"""
            <div class="checkbox-select-multiple %(classes)s">
                %(res_super)s
            </div>
        """ % {
                'classes': " ".join(self.classes),
                'res_super': res_super
            })
        return res
    

