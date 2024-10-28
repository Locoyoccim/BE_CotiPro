from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos),
    path('cotizaciones/<int:pk>/', views.lista_cotizaciones),
    path('crear_usuario/', views.Crear_usuario),
    path('usuario/<int:pk>/', views.usuario),
    path('inventario_list/<int:UserPk>/', views.Inventario_list),
    path('detalle_cotizaciones/', views.detalle_cotizaciones)
]
