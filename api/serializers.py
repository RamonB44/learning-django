from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserData
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend


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
        token = RefreshToken.for_user(user)
        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        # ...
        return token
    
    # def validate(self, attr):
    #     data = super().validate(attr)
    #     refresh = self.get_token(self.user)
    #     data["refresh"] = str(refresh)
    #     data["access"] = refresh.access_token
    #     return data

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        print(decoded_payload)
        # user_uid = decoded_payload['user_id']
        # add filter query
        # data.update({'custom_field': 'custom_data'})
        return data