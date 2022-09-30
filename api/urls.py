from django.urls import path
from .views import MyTokenObtainPairView, MyTokenRefreshView, RegisterView, LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='sign_in'),
    path('login/refresh-token/', MyTokenRefreshView.as_view() , name='token_refresh'),
    path('login/access-token',MyTokenObtainPairView.as_view(),name='access_token'),
    path('register/', RegisterView.as_view(), name="sign_up"),
    path('user/update', RegisterView.as_view() , name="update_user"),
    path("user/delete", RegisterView.as_view(), name="delete")
]