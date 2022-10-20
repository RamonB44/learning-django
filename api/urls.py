from django.urls import path
from .views import MyLoginView, RegisterView, CheckToken, LogoutView, MyTokenRefreshView, MyLoginToken


urlpatterns = [
    path('login/', MyLoginView.as_view(), name='sign_in'),
    
    path('refresh-token/', MyTokenRefreshView.as_view() , name='token_refresh'), # check refresh token and return new access token
    path('access-token/',MyLoginToken.as_view(),name='access_token'), # login with token
   
    path('check-token/', CheckToken.as_view(), name='check_token' ),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('logout/',LogoutView.as_view(), name="logout"),
    
    path('user/update/', RegisterView.as_view() , name="update_user"),
    path("user/delete/", RegisterView.as_view(), name="delete")
]