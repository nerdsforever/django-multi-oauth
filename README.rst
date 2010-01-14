django-multi-oauth
==================

example settings.py
-------------------

from oauth.utils import *

OAUTH_SETTINGS = {
    'TWITTER': {
        OAUTH_SERVER            : 'twitter.com',
        OAUTH_REQUEST_TOKEN_URL : 'https://twitter.com/oauth/request_token', #
        OAUTH_ACCESS_TOKEN_URL  : 'https://twitter.com/oauth/access_token', 
        OAUTH_AUTHORIZATION_URL : 'https://twitter.com/oauth/authorize', 
        OAUTH_CONSUMER_KEY      : '',
        OAUTH_CONSUMER_SECRET   : '',
        OAUTH_TOKEN_NAME        : 'oauth_token',
        OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY: 'twitter_unauthorized_token',

        OAUTH_ACCESS_TOKEN_KEY  : 'twitter_access_token',    # Name of session key used to store access token
        OAUTH_BASE_TEMPLATE     : 'oauth/twitter/main.html', # Base template when /oauth/twitter/ is retrieved
        OAUTH_CALLBACK_REDIRECT_URL_NAME: '',                # Named url of where to redirect to after oauth
        OAUTH_AUTH_REDIRECT_URL_NAME: 'oauth_main',          # Named url of where to redirect to if already auth
    },
    'FRIENDFEED': {
        OAUTH_SERVER            : 'friendfeed.com',
        OAUTH_REQUEST_TOKEN_URL : 'https://friendfeed.com/account/oauth/request_token', 
        OAUTH_ACCESS_TOKEN_URL  : 'https://friendfeed.com/account/oauth/access_token', 
        OAUTH_AUTHORIZATION_URL : 'https://friendfeed.com/account/oauth/authorize', 
        OAUTH_CONSUMER_KEY      : '',
        OAUTH_CONSUMER_SECRET   : '',
        OAUTH_TOKEN_NAME        : 'oauth_token',
        OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY: 'ff_unauthorized_token',
        OAUTH_ACCESS_TOKEN_KEY  : 'ff_access_token',
        OAUTH_BASE_TEMPLATE     : 'oauth/friendfeed/main.html', 
        OAUTH_CALLBACK_REDIRECT_URL_NAME: '',
        OAUTH_AUTH_REDIRECT_URL_NAME: 'oauth_main',
    }
}

