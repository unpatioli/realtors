from django.conf.urls.defaults import *

from buildings.location_dispatcher import LOCATION_FORMS

common_patterns = patterns('buildings.views',
    # (r'/$', 'index'),
    # (r'user/(?P<user_id>\d+)/$', 'user_index'),
)

location_regexp = r"\b%s\b" % r"\b|\b".join([location for location in LOCATION_FORMS])
rentflat_patterns = patterns('buildings.views',
    (r'user/(?P<user_id>\d+)/rent/flats/$', 'user_rentflat_list'),
    (r'rent/flats/(?P<id>\d+)/$', 'rentflat_detail'),
    (r'rent/flats/new/(?P<location>%s)/$' % location_regexp, 'rentflat_new'),
    (r'rent/flats/(?P<id>\d+)/edit/$', 'rentflat_edit'),
    # (r'rent/flats/(?P<id>\d+)/delete/$', 'rentflat_delete')
)

sellflat_patterns = patterns('buildings.views',
    (r'user/(?P<user_id>\d+)/sell/flats/$', 'user_sellflat_list'),
    (r'sell/flats/(?P<id>\d+)/$', 'sellflat_detail'),
    (r'sell/flats/new/(?P<location>%s)/$' % location_regexp, 'sellflat_new'),
    (r'sell/flats/(?P<id>\d+)/edit/$', 'sellflat_edit'),
    # (r'sell/flats/(?P<id>\d+)/delete/$', 'sellflat_delete')
)

search_patterns = patterns('buildings.views',
    (r'search/$', 'search'),
    # (r'find/$', 'find'),
)

urlpatterns = common_patterns + rentflat_patterns + sellflat_patterns + search_patterns