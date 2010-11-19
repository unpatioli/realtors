from django import template

register = template.Library()

class AddParameter(template.Node):
    def __init__(self, varname, value):
        self.varname = varname
        self.value = value
    
    def render(self, context):
        request = context['request']
        params = request.GET.copy()
        params[self.varname] = self.value
        return '%s?%s' % (request.path, params.urlencode())
    

def addurlparameter(parser, token):
    from re import split
    bits = split(r'\s+', token.contents, 2)
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "'%s' tag requires two arguments" % bits[0]
    return AddParameter(bits[1],bits[2])
    
register.tag('addurlparameter', addurlparameter)



class SortHeader(template.Node):
    def __init__(self, varname, value, title, asc_title, desc_title):
        self.varname = varname
        self.value = value
        self.title = title
        self.asc_title = asc_title
        self.desc_title = desc_title
    
    def render(self, context):
        request = context['request']
        params = request.GET.copy()
        sort = params.get(self.varname, "")
        if sort == self.value:
            title = self.title + self.asc_title
            params[self.varname] = "-" + self.value
        elif sort == "-" + self.value:
            title = self.title + self.desc_title
            params[self.varname] = self.value
        else:
            title = self.title
            params[self.varname] = self.value
        return "<a href=%s?%s>%s</a>" % (request.path, params.urlencode(), title)

def sort_header(parser, token):
    from re import split
    bits = split(r'\s+', token.contents, 5)
    if len(bits) < 5:
        raise template.TemplateSyntaxError, "'%s' tag requires five arguments" % bits[0]
    return SortHeader(bits[1],bits[2],bits[3],bits[4],bits[5])

register.tag('sort_header', sort_header)
