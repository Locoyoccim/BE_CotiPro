from django.urls import path
from . import views

urlpatterns = [
    path('productos/<int:pk>/', views.lista_productos),
    path('crear_usuario/', views.Crear_usuario),
    path('usuario/<int:pk>/', views.usuario),
    path('inventario_list/<int:UserPk>/', views.Inventario_list),
    path('detalle_cotizaciones/<int:CotiId>/', views.detalle_cotizaciones),
    path('cotizaciones/<int:pk>/', views.lista_cotizaciones),
]
