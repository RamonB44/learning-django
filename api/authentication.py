from rest_framework_simplejwt.authentication import JWTAuthentication    
from django.conf import settings

class CookieHandlerJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # If cookie contains access token, put it inside authorization header
        access_token = request.COOKIES.get('access_token')
        if(access_token):
            request.META['HTTP_AUTHORIZATION'] = '{header_type} {access_token}'.format(
                header_type=settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0], access_token=access_token)

        return super().authenticate(request)