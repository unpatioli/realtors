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
    

# ====================
# = JQueryUI Widgets =
# ====================
class SliderWidget(forms.TextInput):
    class Media:
        css = {
            'all': ("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.0/themes/base/jquery-ui.css",),
        }
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",
        )
    
    def render(self, name, value, attrs=None):
        from django.utils.safestring import mark_safe
        res = super(SliderWidget, self).render(name, value, attrs=attrs)
        if attrs and 'id' in attrs:
            res += mark_safe(u"""
                <div id="%(id)s_slider"></div>
                <script type="text/javascript">
                    $(function() {
                        $("#%(id)s_slider").slider({
                            value: $("#%(id)s").val(),
                            min: 0,
                            max: 180,
                            slide: function(event, ui){
                                $("#%(id)s").val(ui.value);
                            }
                        });
                        $("#%(id)s").val($("#%(id)s_slider").slider("value"));
                    });
                </script>
            """ % {'id': attrs['id']} )
        return res
    

class AutocompleteWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        self.data_source = []
        if 'data_source' in kwargs:
            self.data_source = kwargs.pop('data_source')
        super(AutocompleteWidget, self).__init__(*args, **kwargs)
    
    class Media:
        css = {
            'all': (
                "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/base/jquery-ui.css",
            ),
        }
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",
        )
    
    def render(self, name, value, attrs=None):
        from django.utils.safestring import mark_safe
        res = super(AutocompleteWidget, self).render(name, value, attrs=attrs)
        if attrs and 'id' in attrs:
            res += mark_safe(u"""
                <script type="text/javascript">
                    $(function(){
                        $( "#%s" ).autocomplete({
                            source: [%s]
                        });
                    });
                </script>
            """ % ( attrs['id'], ",".join(map(lambda x: "\"%s\"" % str(x), self.data_source)) )
            )
        return res

class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/base/jquery-ui.css",
            ),
        }
        js = (
            "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",
            "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/i18n/jquery-ui-i18n.min.js",
        )
    
    def render(self, name, value, attrs=None):
        from django.utils.safestring import mark_safe
        res = super(CalendarWidget, self).render(name, value, attrs=attrs)
        if attrs and 'id' in attrs:
            res += mark_safe(u"""
                <script type="text/javascript">
                    $(function() {
                        $.datepicker.setDefaults( $.datepicker.regional[ "ru" ] );
                        $( "#%s" ).datepicker({
                                changeYear: true,
                                changeMonth: true,
                                yearRange: '-90:+00',
                                defaultDate: '-18y'
                            });
                    });
                </script>
            """ % attrs['id'])
        return res
    

