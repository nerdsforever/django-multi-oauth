from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from utils import *
import oauth, httplib, logging

CONSUMERS      = {}
CONNECTIONS    = {}
OAUTH_SETTINGS = settings.OAUTH_SETTINGS

def oauth_main(request, service):
    return render_to_response(get_oauth_var(service, OAUTH_BASE_TEMPLATE), 
                              {service: 'service'},
                              context_instance=RequestContext(request))

def oauth_auth(request, service):
    access_token_key = get_oauth_var(service, OAUTH_ACCESS_TOKEN_KEY)
    if not request.session.has_key(access_token_key):
        request_token_url = get_oauth_var(service, OAUTH_REQUEST_TOKEN_URL)
        request_token     = get_unauthorized_request_token(get_consumer(service),
                                                           get_connection(service),
                                                           request_token_url)
        
        auth_url          = get_oauth_var(service, OAUTH_AUTHORIZATION_URL)
        authorization_url = get_authorization_url(get_consumer(service), 
                                                  request_token, 
                                                  auth_url)

        unauth_request_token_key = get_oauth_var(service, 
                                                 OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY)
        request.session[unauth_request_token_key] = request_token.to_string()
        return HttpResponseRedirect(authorization_url)
    else:
        return HttpResponse("Failsauce: You have already been authenticated!")

def oauth_clear_auth(request, service):
    request.session.clear()
    return HttpResponseRedirect(reverse('oauth_main', args=[service]))

def oauth_callback(request, service):
    unauth_request_token_key = get_oauth_var(service, 
                                             OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY)
    unauthorized_token = request.session.get(unauth_request_token_key, None)
    if not unauthorized_token:
        return HttpResponse("Failsauce: No un-authed token stored in session")

    token = oauth.OAuthToken.from_string(unauthorized_token)   

    oauth_token_name = get_oauth_var(service, OAUTH_TOKEN_NAME)
    if token.key != request.GET.get(oauth_token_name, None):
        return HttpResponse("Failsauce: Tokens do not match")

    access_token_url = get_oauth_var(service, OAUTH_ACCESS_TOKEN_URL)
    access_token = exchange_request_token_for_access_token(get_consumer(service), 
                                                           get_connection(service),
                                                           access_token_url,
                                                           token)

    access_token_key = get_oauth_var(service, OAUTH_ACCESS_TOKEN_KEY)
    request.session[access_token_key] = access_token.to_string()

    redirect_url_name = get_oauth_var(service, OAUTH_CALLBACK_REDIRECT_URL_NAME)
    return HttpResponseRedirect(reverse(redirect_url_name))

# View helpers
def get_consumer(service):
    service_upper = service.upper()
    if not CONSUMERS.has_key(service_upper):
        consumer_key = get_oauth_var(service, OAUTH_CONSUMER_KEY)
        consumer_sec = get_oauth_var(service, OAUTH_CONSUMER_SECRET)
        CONSUMERS[service_upper] = oauth.OAuthConsumer(consumer_key, 
                                                       consumer_sec)
    return CONSUMERS[service_upper]

def get_connection(service):
    service_upper = service.upper()
    if not CONNECTIONS.has_key(service_upper):
        server = get_oauth_var(service, OAUTH_SERVER)
        CONNECTIONS[service_upper] = httplib.HTTPSConnection(server)
    return CONNECTIONS[service_upper]

def get_oauth_var(service, variable_key, settings=OAUTH_SETTINGS):
    """ Helper to return OAuth variables from settings file """
    return get_oauth_variable(service, variable_key, settings)
