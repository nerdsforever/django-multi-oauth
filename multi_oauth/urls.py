# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('oauth.views',
    url(r'^(?P<service>\w+)/$', 'oauth_main', name='oauth_main'),
    url(r'^(?P<service>\w+)/auth/$', 'oauth_auth', name='oauth_auth'),
    url(r'^(?P<service>\w+)/clear_auth/$', 'oauth_clear_auth', name='oauth_clear_auth'),
    url(r'^(?P<service>\w+)/callback/$', 'oauth_callback', name='oauth_callback'),
) 
