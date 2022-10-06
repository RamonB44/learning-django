from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, Token
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
        data = {
                'user':{
                    "uuid" : user.id,
                    "from" : "",
                    "role": "admin",# estos es importante para poder logear
                    "data": {
                        "displayName": user.name,
                        "photoURL": "",
                        "email": user.email,
                        "settings":{
                            "layout": { },
                            "theme": { }
                        },
                        "shortcuts": []
                    }
                },
                'access_token' : str(refresh.access_token)
            }

        return Response(data, status= status.HTTP_200_OK)
        
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
    def get(self, request):
        pass
    
class MyLoginToken(APIView):
    def get(self, request):
        res = JWT_authenticator.authenticate(request)
        if res is not None:
            user , token = res
            #aqui debe refrescarse la sesion
            #print(user.password)
            data = {
                'user':{
                    "uuid" : user.id,
                    "from" : "",
                    "role": "admin",# estos es importante para poder logear
                    "data": {
                        "displayName": user.name,
                        "photoURL": "",
                        "email": user.email,
                        "settings":{
                            "layout": { },
                            "theme": { }
                        },
                        "shortcuts": []
                    }
                },
                'access_token' : str(token)
            }
            return Response(data)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer