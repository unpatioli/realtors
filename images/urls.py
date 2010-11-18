from django.conf.urls.defaults import *

contenttypes_regexp = r"\b%s\b" % r"\b|\b".join(['rentflat', 'sellflat'])

urlpatterns = patterns('images.views',
    url(    r'(?P<content_type>%s)/(?P<object_id>\d+)/$' % contenttypes_regexp,
            'object_image_list',
            name = 'images_object_image_list'
    ),
    url(    r'(?P<content_type>%s)/(?P<object_id>\d+)/new$' % contenttypes_regexp,
            'object_image_new',
            name = 'images_object_image_new'
    ),
    url(    r'(?P<content_type>%s)/(?P<object_id>\d+)/(?P<id>\d+)/edit$' % contenttypes_regexp,
            'object_image_edit',
            name = 'images_object_image_edit'
    ),
    url(    r'(?P<content_type>%s)/(?P<object_id>\d+)/(?P<id>\d+)/delete$' % contenttypes_regexp,
            'object_image_delete',
            name = 'images_object_image_delete'
    ),
)
