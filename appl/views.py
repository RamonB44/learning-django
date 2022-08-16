import json
from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import Company

# Create your views here.
# def index(req):
#     return HttpResponse("Hi, im Django")


class CompanyView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, req, id: 0):
        if id > 0:
            companies = list(Company.objects.filter(id=id).values())
            if len(companies) > 0:
                company = companies[0]
                datos = {"message": "Success", 'company': company}
            else:
                datos = {"message": "Companies not found ..."}
                return JsonResponse(datos)
        else:
            companies = list(Company.objects.values())
            if len(companies) > 0:
                datos = {"message": "Success", 'companies': companies}
            else:
                datos = {"message": "Companies not found ..."}
            return JsonResponse(datos)

    def post(self, req):
        print(req.body)
        in_data = json.loads(req.body)
        # print(in_data)
        Company.objects.create(
            name=in_data["name"], website=in_data["website"], foundation=in_data["foundation"])
        datos = {"message": "Success"}
        return JsonResponse(datos)

    def put(self, req, id):
        injd = json.loads(req.body)
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            company = Company.objects.get(id=id)
            company.name = injd["name"]
            company.website = injd["website"]
            company.foundation = injd["foundation"]
            company.save()
            datos = {"message": "Success"}
        else:
            datos = {"message": "Companies not found ..."}

        return JsonResponse(datos)

    def delete(self, req, id):
        companies = list(Company.objects.filter(id=id).values())
        if len(companies) > 0:
            Company.objects.filter(id=id).delete()
            datos = {"message": "Success"}
        else:
            datos = {"message": "Company not found ..."}
        return JsonResponse(datos)
