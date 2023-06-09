from django.shortcuts import render
from rest_framework.views import APIView
from .models import Epp
from .serializers import EppSerializer

# Create your views here.
class EppView(APIView):
    queryset = Epp.objects.all()
    serializer_class = EppSerializer
    def post():
        pass
    def get():
        pass
    def put():
        pass
    def delete():
        pass
    