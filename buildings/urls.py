from django.conf.urls.defaults import *

rentflat_patterns = patterns('buildings.views',
    (r'^rent/flats$', 'rentflat_list'),
    (r'^rent/flats/(?P<id>\d+)$', 'rentflat_detail'),
    (r'^rent/flats/new$', 'rentflat_new'),
    (r'^rent/flats/edit/(?P<id>\d+)', 'rentflat_edit'),
    (r'^rent/flats/delete/(?P<id>\d+)', 'rentflat_delete')
)

sellflat_patterns = patterns('buildings.views',
    (r'^sell/flats$', 'sellflat_list'),
    (r'^sell/flats/(?P<id>\d+)$', 'sellflat_detail'),
    (r'^sell/flats/new$', 'sellflat_new'),
    (r'^sell/flats/edit/(?P<id>\d+)', 'sellflat_edit'),
    (r'^sell/flats/delete/(?P<id>\d+)', 'sellflat_delete')
)

urlpatterns = patterns('buildings.views', (r'^$', 'index')) + \
    rentflat_patterns + \
    sellflat_patterns