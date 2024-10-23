import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Productos, Cotizaciones, Usuarios

# Create your views here.
@csrf_exempt
def Crear_usuario(request):
    if request.method == 'POST':
        return Nuevo_usuario(request)

@csrf_exempt
def Actualizar_usuario(request, pk):
    if request.method == 'PUT':
        data = json.loads(request.body)

        usuario = get_object_or_404(Usuarios, id=pk)
        usuario.empresa = data["empresa"]
        usuario.nombre = data["nombre"]
        usuario.email = data["email"]
        usuario.rol = data["rol"]
        usuario.save()

        return JsonResponse('Actualizacion completa', status=200, safe=False) 

    else:
        return JsonResponse('Method invalido para actualizar', status=405, safe=False)

def Obtener_usuario(request, pk):
    if request.method == 'GET':
        usuario = get_object_or_404(Usuarios, id=pk)
        return JsonResponse(usuario.usuario_dict(), safe=False)
    else:
        return JsonResponse('Method invalido para obtener', status=405, safe=False)

@csrf_exempt
def lista_productos(request):
    if request.method == 'GET':
        return Obtener_Productos(request)
    elif request.method == 'POST':
        return Crear_producto(request)
    elif request.method == 'DELETE':
        return Eliminar_producto(request)
    elif request.method == 'PUT':
        return Actualizar_producto(request)
    else:
        return HttpResponse("Metodo Invalido", status=405)

def lista_cotizaciones(request):
    cotizaciones = list(Cotizaciones.objects.all().values())

    return JsonResponse(cotizaciones, safe=False)

# FUNCIONES USUARIOS
def Nuevo_usuario(request):
    data = json.loads(request.body)

    required_fields = ['empresa', 'nombre', 'email', 'password', 'rol']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'El campo {field} es requerido.'}, status=400)
        
    Usuario = Usuarios.objects.create(
        empresa=data['empresa'],
        nombre=data['nombre'], 
        email=data['email'],
        password=data['password'],
        rol=data['rol']
    )

    Usuario.save()

    response = {
        'message': 'Usuario creado con éxito',
        'usuario': {
            'id': Usuario.id,
            'empresa': Usuario.empresa,
            'nombre': Usuario.nombre,
            'email': Usuario.email,
            'rol': Usuario.rol,
        }
    }

    return JsonResponse(response, safe=False)

# FUNCIONES PARA PRODUCTOS
def Obtener_Productos(request):
    productos = list(Productos.objects.all().values())

    return JsonResponse(productos, safe=False)

def Crear_producto(request):
    data = json.loads(request.body)

     # Validar que todos los campos requeridos están presentes
    required_fields = ['id_user', 'nombre', 'tipo_producto', 'unidad_medida', 'descripcion', 'costo', 'precio']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'El campo {field} es requerido.'}, status=400)

    usuario_id = get_object_or_404(Usuarios, id=data['id_user']) 

    producto = Productos.objects.create(
        id_user = usuario_id,
        nombre = data['nombre'],
        tipo_producto = data['tipo_producto'],
        unidad_medida = data['unidad_medida'],
        descripcion = data['descripcion'],
        costo = data['costo'],
        precio = data['precio']
    )

    producto.save()

    response = {
        'message': 'Producto creado con éxito',
        'producto': {
            'id': producto.pk_producto,
            'nombre': producto.nombre,
            'tipo_producto': producto.tipo_producto,
            'unidad_medida': producto.unidad_medida,
            'descripcion': producto.descripcion,
            'costo': producto.costo,
            'precio': producto.precio
        }
    }

    return JsonResponse(response, status=201)

def Eliminar_producto(request):
    data = json.loads(request.body)

    producto = get_object_or_404(Productos, pk_producto=data["pk_producto"])
    producto.delete()

    return JsonResponse({'message': 'Producto eliminado con éxito'}, status=200)

def Actualizar_producto(request):
    data = json.loads(request.body)

    if "pk_producto" not in data:
        return JsonResponse('Producto eliminado o no encontrado', status=400)

    producto = get_object_or_404(Productos, pk_producto=data["pk_producto"])

    producto.nombre = data["nombre"]
    producto.tipo_producto = data["tipo_producto"]
    producto.unidad_medida = data["unidad_medida"]
    producto.descripcion = data["descripcion"]
    producto.costo = data["costo"]
    producto.precio = data["precio"]
    producto.save()

    return JsonResponse({'message': 'Producto actualizado con éxito'}, status=200)

# FUNCIONES PARA COTIZACIONES
