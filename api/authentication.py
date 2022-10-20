from rest_framework_simplejwt.authentication import JWTAuthentication    
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

def enforce_csrf(request):
    check = CSRFCheck(dummy_get_response)
    check.process_request(request)

    reason = check.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
    
def dummy_get_response(request):  # pragma: no cover
    return None

class CookieHandlerJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        
        if header is None:
            # print("no hay header")
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            # print("existe header")
            raw_token = self.get_raw_token(header)
            
        if raw_token is None:
            return None
        
        try:
            validated_token = self.get_validated_token(raw_token)
            enforce_csrf(request)
        
            if(validated_token):
                request.META['HTTP_AUTHORIZATION'] = '{header_type} {access_token}'.format(
                    header_type=settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0], access_token=validated_token)

            return super().authenticate(request)
        except InvalidToken:
            print("invalidToken")
            return None