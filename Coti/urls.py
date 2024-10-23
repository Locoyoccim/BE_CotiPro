from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos),
    path('cotizaciones/', views.lista_cotizaciones),
    path('crear_usuario/', views.Crear_usuario),
    path('actualizar_usuario/<int:pk>/', views.Actualizar_usuario),
    path('obtener_usuario/<int:pk>/', views.Obtener_usuario)
]
