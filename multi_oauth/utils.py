import oauth

HMAC_SIGNATURE_METHOD  = oauth.OAuthSignatureMethod_HMAC_SHA1()

OAUTH_SERVER            = 'OAUTH_SERVER'
OAUTH_REQUEST_TOKEN_URL = 'OAUTH_REQUEST_TOKEN_URL'
OAUTH_ACCESS_TOKEN_URL  = 'OAUTH_ACCESS_TOKEN_URL'
OAUTH_AUTHORIZATION_URL = 'OAUTH_AUTHORIZATION_URL'
OAUTH_CONSUMER_KEY      = 'OAUTH_CONSUMER_KEY'
OAUTH_CONSUMER_SECRET   = 'OAUTH_CONSUMER_SECRET'      
OAUTH_TOKEN_NAME        = 'OAUTH_TOKEN_NAME'    
OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY = 'OAUTH_UNAUTHORIZED_REQUEST_TOKEN_KEY'
OAUTH_ACCESS_TOKEN_KEY  = 'OAUTH_ACCESS_TOKEN_KEY'
OAUTH_BASE_TEMPLATE     = 'OAUTH_BASE_TEMPLATE'
OAUTH_CALLBACK_REDIRECT_URL_NAME = 'OAUTH_CALLBACK_REDIRECT_URL_NAME'
OAUTH_AUTH_REDIRECT_URL_NAME = 'OAUTH_AUTH_REDIRECT_URL_NAME'

class OAuthConfigurationError(Exception):
    pass

def request_oauth_resource(consumer, 
                           url, 
                           access_token, 
                           parameters=None, 
                           signature_method=HMAC_SIGNATURE_METHOD, 
                           http_method="GET"):

    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, 
        token=access_token, 
        http_method=http_method, 
        http_url=url, 
        parameters=parameters,
    )
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request

def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    connection.request(oauth_request.http_method, url)
    response = connection.getresponse()
    output = response.read()
    return output

def get_unauthorized_request_token(consumer, 
                                   connection,
                                   request_token_url,
                                   signature_method=HMAC_SIGNATURE_METHOD,parameters=None):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, http_url=request_token_url, parameters = parameters
    )
    oauth_request.sign_request(signature_method, consumer, None)
    response = fetch_response(oauth_request, connection)
    token = oauth.OAuthToken.from_string(response)
    return token

def get_authorization_url(consumer, 
                          token, 
                          authorization_url,
                          signature_method=HMAC_SIGNATURE_METHOD,**kwargs):
    parameters = kwargs.pop('parameters',None)
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=token, http_url=authorization_url, parameters = parameters
    )
    oauth_request.sign_request(signature_method, consumer, token)
    url = oauth_request.to_url()
    return url

def exchange_request_token_for_access_token(consumer, 
                                            connection, 
                                            access_token_url,
                                            request_token, 
                                            signature_method=HMAC_SIGNATURE_METHOD):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=request_token, http_url=access_token_url
    )
    oauth_request.sign_request(signature_method, consumer, request_token)
    response = fetch_response(oauth_request, connection)
    return oauth.OAuthToken.from_string(response) 

def get_oauth_variable(service, variable_name, configuration):
    service_upper = service.upper()
    if isinstance(configuration, dict):
        if configuration.has_key(service_upper):
            return configuration[service_upper][variable_name]
        else:
            raise OAuthConfigurationError("No configuration settings for the %s service." % service)
    else:
        raise OAuthConfigurationError("OAuthConfiguration must be a dictionary!")
