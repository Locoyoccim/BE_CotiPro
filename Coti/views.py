from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Productos, Cotizaciones

# Create your views here.
def lista_productos(request):
    productos = Productos.objects.all().values()

    return JsonResponse(list(productos), safe=False)

def lista_cotizaciones(request):
    cotizaciones = Cotizaciones.objects.all()

    return JsonResponse(cotizaciones, safe=False)