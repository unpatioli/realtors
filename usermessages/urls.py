from django.conf.urls.defaults import *

urlpatterns = patterns('usermessages.views',
    url(    r'inbox/$',
            'message_list',
            {'box_type': 'inbox'},
            name = 'usermessages_message_list'
    ),
    url(    r'outbox/$',
            'message_list',
            {'box_type': 'outbox'},
            name = 'usermessages_message_list'
    ),
    url(    r'trash/$',
            'message_list',
            {'box_type': 'trash'},
            name = 'usermessages_message_list'
    ),
    
    url(    r'new/$',
            'message_new',
            name = 'usermessages_message_new'
    ),
    url(    r'(?P<object_id>\d+)/edit$',
            'message_edit',
            name = 'usermessages_message_edit'
    ),
    url(    r'(?P<object_id>\d+)/delete$',
            'message_delete',
            name = 'usermessages_message_delete'
    ),
)
