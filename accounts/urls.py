from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logged_out.html'}),
    (r'^register/$', 'accounts.views.register'),
    (r'^profile/(?P<user_id>\d+)/$', 'accounts.views.profile'),
    (r'^profile/$', 'accounts.views.my_profile'),
    (r'^profile/new/$', 'accounts.views.my_profile_new'),
    (r'^profile/edit/$', 'accounts.views.my_profile_edit'),
)
