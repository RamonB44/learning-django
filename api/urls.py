from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, RegisterView ,MyLoginToken#, LoginView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='sign_in'),
    path('refresh-token/', MyTokenRefreshView.as_view() , name='token_refresh'), # check refresh token and return new access token
    path('access-token/',MyLoginToken.as_view(),name='access_token'), # login with token and generate a new refresh, access token
    
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('user/update/', RegisterView.as_view() , name="update_user"),
    path("user/delete/", RegisterView.as_view(), name="delete")
]