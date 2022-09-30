from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data = serializer.validated_data
        user = authenticate(email=data['email'], password=data['password'])
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
                'email': user.email,
                'access': str(refresh.access_token),          
        }, status= status.HTTP_200_OK)
        
    def put(self, request):
        pass
    
    def delete(self, request):
        pass
    
    def get(self, request):
        pass
    
#view for log-in
class LoginView(APIView):
    def post(self, request):
        print(request)
        return Response(request)
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer