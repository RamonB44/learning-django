import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.middleware import csrf
#from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

#    permission_classes = (IsAuthenticated,)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# view for registering users
class RegisterView(APIView):
    def post(self, request):
        dt = request.data
        dt["name"] = dt["displayName"]
        
        serializer = UserSerializer(data=dt)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.validated_data
        
        user = authenticate(email=data['email'], password=data['password'])
        
        refresh = RefreshToken.for_user(user)
        user_group = user.groups.values_list('name', flat=True)[0]
        structure = open('./api/user_data.json')
        data = json.load(structure)
        data['user']['uuid'] = user.id
        data['user']['role'] = user_group
        data['user']['data']['displayName'] =  user.name
        data['user']['data']['photoURL'] =  user.photoURL
        data['user']['data']['email'] =  user.email
        data['user']['data']['settings']['customScrollbars'] = True
        res = Response(data, status= status.HTTP_200_OK)
        
        return res

class MyLoginView(APIView):
    def post(self, request):
        data = request.data
        response = Response()        
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = data["access"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","data":data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

# JWT_authenticator = JWTAuthentication()
# class MyLoginToken(APIView):
#     def post(self, request):
#         # checks the validity of the token in the header and returns both the token and user data
#         res = JWT_authenticator.authenticate(request)
#         if res is not None:
#             user , _token = res
#             #add to blacklist
#             invalidate_token = RefreshToken(request.data['refresh'])
#             invalidate_token.verify()
#             invalidate_token.blacklist()
#             # generate a new access and refresh token
#             refresh = RefreshToken.for_user(user)
#             # the new desired expiration time for the new token is added
#             # refresh.set_exp()
#             user_group = user.groups.values_list('name', flat=True)[0]
#             structure = open('./api/user_data.json')
#             data = json.load(structure)
#             data['user']['uuid'] = user.id
#             data['user']['role'] = user_group
#             data['user']['data']['displayName'] =  user.name
#             data['user']['data']['photoURL'] =  user.photoURL
#             data['user']['data']['email'] =  user.email
#             data['user']['data']['settings']['customScrollbars'] = True
#             data["refresh"] = str(refresh)
#             data["access_token"] = str(refresh.access_token)
#             return Response(data, status= status.HTTP_200_OK)