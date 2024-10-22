from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
]
