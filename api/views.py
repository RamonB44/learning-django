import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

#    permission_classes = (IsAuthenticated,)
# view for registering users
JWT_authenticator = JWTAuthentication()
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
        data["refresh"] = str(refresh)
        data["access_token"] = str(refresh.access_token)

        return Response(data, status= status.HTTP_200_OK)
        
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
    def get(self, request):
        pass
    
class MyLoginToken(APIView):
    def post(self, request):
        # checks the validity of the token in the header and returns both the token and user data
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user , _token = res
            #add to blacklist
            invalidate_token = RefreshToken(request.data['refresh'])
            invalidate_token.verify()
            invalidate_token.blacklist()
            # generate a new access and refresh token
            refresh = RefreshToken.for_user(user)
            # the new desired expiration time for the new token is added
            # refresh.set_exp()
            user_group = user.groups.values_list('name', flat=True)[0]
            structure = open('./api/user_data.json')
            data = json.load(structure)
            data['user']['uuid'] = user.id
            data['user']['role'] = user_group
            data['user']['data']['displayName'] =  user.name
            data['user']['data']['photoURL'] =  user.photoURL
            data['user']['data']['email'] =  user.email
            data['user']['data']['settings']['customScrollbars'] = True
            data["refresh"] = str(refresh)
            data["access_token"] = str(refresh.access_token)
            return Response(data, status= status.HTTP_200_OK)
    
class CheckToken(APIView):
    def post(self, request):
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user , _token = res
            data = { "access_token" : _token }
            return Response(data , status= status.HTTP_200_OK)
        return Response({"access_token" : ""} , status= status.HTTP_200_OK )

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer