from django.urls import path
from .views import EppView

urlpatterns = [
   path('epp/', EppView.as_view(), name='EppView'),
]