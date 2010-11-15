from django.conf.urls.defaults import *

from buildings.location_dispatcher import LOCATION_FORMS, LocationDispatcher

common_patterns = patterns('buildings.views',
    # (r'/$', 'index'),
    # (r'user/(?P<user_id>\d+)/$', 'user_index'),
)

location_regexp = r"\b%s\b" % r"\b|\b".join([location for location in LOCATION_FORMS])
deal_type_regexp = r"\b%s\b" % r"\b|\b".join([deal_type[0] for deal_type in LocationDispatcher.deal_types()])

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

# search_patterns = patterns('buildings.views',
#     (r'search/(?P<deal_type>%(deal_type)s)/(?P<location>%(location)s)/$' % {
#         'deal_type': deal_type_regexp,
#         'location': location_regexp,
#         }, 'search'),
#     # (r'find/$', 'find'),
# )
search_patterns = patterns('buildings.views',
    url(    r'search/rent/flat/moscow/$',
            'moscow_rentflat_search',
            name = 'buildings_moscow_rentflat_search'
    ),
    url(    r'search/rent/flat/moscow_region/$',
            'moscow_region_rentflat_search',
            name = 'buildings_moscow_region_rentflat_search'
    ),
    url(    r'search/rent/flat/common/$',
            'common_rentflat_search',
            'buildings_common_rentflat_search'
    ),
    
    url(    r'search/sell/flat/moscow/$',
            'moscow_sellflat_search',
            'buildings_moscow_sellflat_search'
    ),
    url(    r'search/sell/flat/moscow_region/$',
            'moscow_region_sellflat_search',
            'buildings_moscow_region_sellflat_search'
    ),
    url(    r'search/sell/flat/common/$',
            'common_sellflat_search',
            'buildings_common_sellflat_search'
    ),
)

urlpatterns = common_patterns + rentflat_patterns + sellflat_patterns + search_patterns