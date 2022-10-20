from datetime import timedelta
import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.middleware import csrf
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

#    permission_classes = (IsAuthenticated,)
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access-token': str(refresh.access_token),
    }
# view for registering users
class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        dt = request.data
        dt["name"] = dt["displayName"]
        
        serializer = UserSerializer(data=dt)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.validated_data
        res = Response()
        user = authenticate(email=data['email'], password=data['password'])
        
        data = get_tokens_for_user(user)
        
        user_group = user.groups.values_list('name', flat=True)[0]
        structure = open('./api/user_data.json')
        
        _data = json.load(structure)
        _data['user']['uuid'] = user.id
        _data['user']['role'] = user_group
        _data['user']['data']['displayName'] =  user.name
        _data['user']['data']['photoURL'] =  user.photoURL
        _data['user']['data']['email'] =  user.email
        _data['user']['data']['settings']['customScrollbars'] = True
        
        res.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value = data["access-token"],
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
                
        res.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_REFRESH'], 
            value = data["refresh"],
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
                
        csrf.get_token(request)
        res.data = { "Success" : "Usuario registrado", "user": _data }
        return res

class MyLoginView(APIView):
    permission_classes = []
    def post(self, request):
        data = request.data
        response = Response()
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                
                user_group = user.groups.values_list('name', flat=True)[0]
                structure = open('./api/user_data.json')
                
                _data = json.load(structure)
                _data['uuid'] = user.id
                _data['role'] = user_group
                _data['data']['displayName'] =  user.name
                _data['data']['photoURL'] =  user.photoURL
                _data['data']['email'] =  user.email
                _data['data']['settings']['customScrollbars'] = True
                
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                    value = data["access-token"],
                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                
                response.set_cookie(
                    key = settings.SIMPLE_JWT['AUTH_REFRESH'], 
                    value = data["refresh"],
                    expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                
                csrf.get_token(request)
                response.data = {"Success" : "Login successfully","user":_data}
                return response
            else:
                return Response({"No active" : "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            #validar si usuario existe
            return Response({"Invalid" : "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)

class CheckToken(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        res = Response()
        res.data = { 'is_valid' : True ,}
        return res
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        pass
    
# JWT_authenticator = JWTAuthentication()
class MyLoginToken(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        # checks the validity of the token in the header and returns both the token and user data
        current_user = request.user
        response = Response()
        
        refresh = RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT['AUTH_REFRESH']) or None)
        
        user_group = current_user.groups.values_list('name', flat=True)[0]
        structure = open('./api/user_data.json')
        data = json.load(structure)
        data['uuid'] = current_user.id
        data['role'] = user_group
        data['data']['displayName'] =  current_user.name
        data['data']['photoURL'] =  current_user.photoURL
        data['data']['email'] =  current_user.email
        data['data']['settings']['customScrollbars'] = True
        # csrf.get_token(request)
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value = refresh.access_token,
            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.data = {"Success" : "Login JWT Token successfully", "user": data}
        return response
    
class MyTokenRefreshView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self,request):
        res = Response()
        try:
            invalidate_token = RefreshToken(request.COOKIES.get(settings.SIMPLE_JWT['AUTH_REFRESH']) or None)
            invalidate_token.verify()
            newToken = invalidate_token.access_token
            res.set_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value = newToken,
                expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        
            res.data = {"message" : "RefreshToken valido"}
            return res
        except TokenError:
            return Response({"message": "Refresh Token Expired"}, status.HTTP_400_BAD_REQUEST)
        
        
        #print(newToken)
