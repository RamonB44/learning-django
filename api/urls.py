from django.urls import path
from .views import MyLoginView, RegisterView, CheckToken, LogoutView, MyTokenRefreshView, MyLoginToken


urlpatterns = [
    # Endpoint for user login. 
    # MyLoginView should authenticate the user and return a success response if the authentication is successful.
    path('login/', MyLoginView.as_view(), name='sign_in'),
    
    # Endpoint for refreshing JWT token. 
    # MyTokenRefreshView should take a valid refresh token and return a new access token.
    path('refresh-token/', MyTokenRefreshView.as_view() , name='token_refresh'), 
    
    # Endpoint for getting access token from refresh token. 
    # MyLoginToken should validate the refresh token and return a new access token.
    path('access-token/',MyLoginToken.as_view(),name='access_token'), 
   
    # Endpoint for checking the validity of a token. 
    # CheckToken should validate the provided token and return whether it's valid or not.
    path('check-token/', CheckToken.as_view(), name='check_token' ),
    
    # Endpoint for user registration. 
    # RegisterView should take user data, validate it, and create a new user if the data is valid.
    path('register/', RegisterView.as_view(), name="sign_up"),
    
    # Endpoint for logging out the user. 
    # LogoutView should invalidate the user's token and end their session.
    path('logout/',LogoutView.as_view(), name="logout"),
    
    # Endpoint for updating user information.
    # This currently uses RegisterView, but should ideally use a separate view that handles user data updates.
    path('user/update/', RegisterView.as_view() , name="update_user"),
    
    # Endpoint for deleting a user.
    # This currently uses RegisterView, but should ideally use a separate view that handles user deletion.
    path("user/delete/", RegisterView.as_view(), name="delete")
]
