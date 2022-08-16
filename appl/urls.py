from nturl2path import url2pathname
from django.urls import path

from .models import Company
from . import views

urlpatterns = [
    path('companies/', views.CompanyView.as_view(), name="companies_list"),
    path('companies/<int:id>', views.CompanyView.as_view(), name="companies_delete")
]