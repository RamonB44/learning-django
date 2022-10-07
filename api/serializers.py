from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .models import UserData
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, validated_data):
        pass
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # we will see this data after decode hash
        # Add custom claims
        token['name'] = user.name
        # ...
        return token
    
    def validate(self, attrs):
        #check first if email exists
        try:
            UserData.objects.get(email=self.username_field)
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed(
                "Email incorrecto",
                "no_email_account",
            )
        #check if credentials is valid
        data = super().validate(attrs)
        #get refresh & token from user
        refresh = self.get_token(self.user)
        #get group name from user
        user_group = self.user.groups.values_list('name', flat=True)[0]
        user = {
            "uuid" : self.user.id,
            "from" : "",
            "role": user_group,# estos es importante para poder logear
            "data": {
                "displayName": self.user.name,
                "photoURL": self.user.photoURL,
                "email": self.user.email,
                "settings":{
                    "layout": { },
                    "theme": { }
                },
                "shortcuts": []
            }
        }
        data['user'] = user
        data["refresh"] = str(refresh)
        data["access_token"] = str(refresh.access_token)
        return data

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        #print(decoded_payload)
        # user_uid = decoded_payload['user_id']
        # add filter query
        # data.update({'custom_field': 'custom_data'})
        return data