import json
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Productos, Cotizaciones, DetalleCotizaciones, Usuarios, Inventario

# Create your views here.
@csrf_exempt
def Crear_usuario(request):
    if request.method == 'POST':
        return Nuevo_usuario(request)
    else:
        return JsonResponse('Method invalido para obtener', status=405, safe=False)

@csrf_exempt
def usuario(request, pk):
    if request.method == 'PUT':
       return actualizar_usuario(request, pk)
    elif request.method == 'GET':
        return get_usuario(request, pk)
    elif request.method == 'DELETE':
        return delete_usuario(request, pk)

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

@csrf_exempt
def Inventario_list(request, UserPk):
    if request.method == 'GET':
        return Obtener_inventario(request, UserPk)
    else:  
        return HttpResponse("Metodo Invalido", status=405)

@csrf_exempt
def lista_cotizaciones(request, pk):
    # ESTAS FUNCIONES AFECTAN LAS TABLAS Cotizaciones & DetalleCotizaciones excepto GET
    if request.method == 'GET':
        return get_cotizaciones(request, pk)
    if request.method == 'POST':
        return nueva_cotizacion(request, pk)
    if request.method == 'PUT':
        return actualizar_cotizacion(request, pk)
    if request.method == 'DELETE':
        return eliminar_cotizacion(request)
    else:  
        return HttpResponse("Metodo Invalido", status=405)
     
def detalle_cotizaciones(request):
    if request.method == 'GET':
        detalles = list(DetalleCotizaciones.objects.all().values())

        return JsonResponse(detalles, safe=False)

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

def actualizar_usuario(request, PK):
    data = json.loads(request.body)

    usuario = get_object_or_404(Usuarios, id=PK)
    usuario.empresa = data["empresa"]
    usuario.nombre = data["nombre"]
    usuario.email = data["email"]
    usuario.rol = data["rol"]
    usuario.save()

    return JsonResponse('Actualizacion completa', status=200, safe=False) 

def get_usuario(request, pk):
    usuario = get_object_or_404(Usuarios, id=pk).usuario_dict()
    
    return JsonResponse(usuario, safe=False)

def delete_usuario(request, pk):
    usuario = get_object_or_404(Usuarios, id=pk)
    name_user = usuario.nombre
    usuario.delete()

    return JsonResponse(f'{name_user} eliminado con exito', safe=False, status=200)

# FUNCIONES PARA PRODUCTOS
def Obtener_Productos(request):
    productos = list(Productos.objects.all().values())

    return JsonResponse(productos, safe=False)

def Crear_producto(request):
    data = json.loads(request.body)

     # Validar que todos los campos requeridos están presentes
    required_fields = ['id_user', 'unidad_medida','tipo_producto', 'descripcion', 'fecha_actualizacion', 'stock_actual', 'stock_sugerido', 'costo', 'precio']
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

    # SE AGREGA AL INVENTARIO
    producto_BD = get_object_or_404(Productos, pk_producto=producto.pk_producto)

    nuevo_inventario = Inventario.objects.create(
        id_user = usuario_id,
        id_producto = producto_BD,
        fecha_actualizacion = data['fecha_actualizacion'],
        tipo = producto_BD.tipo_producto,
        descripcion = producto_BD.descripcion,
        stock_actual = data['stock_actual'],
        stock_sugerido = data['stock_sugerido'],
    )
    nuevo_inventario.save()

    response = {
        'message': 'Producto creado con éxito',
        'producto': {
            'id_producto': producto.pk_producto,
            'nombre': producto.nombre,
            'tipo_producto': producto.tipo_producto,
            'unidad_medida': producto.unidad_medida,
            'descripcion': producto.descripcion,
            'costo': producto.costo,
            'precio': producto.precio,
            'stock_sugerido': data['stock_sugerido'],
            'stock_actual': data['stock_actual']
        }
    }

    return JsonResponse(response, status=201)

def Eliminar_producto(request):
    # Con esta función se elimina el producto de la tabla producto y del inventario
    data = json.loads(request.body)

    producto = get_object_or_404(Productos, pk_producto=data["pk_producto"])
    producto.delete()

    return JsonResponse({'message': 'Producto eliminado con éxito'}, status=200)

def Actualizar_producto(request):
    data = json.loads(request.body)

    if "pk_producto" not in data:
        return JsonResponse('Producto eliminado o no encontrado', status=400)

    producto = get_object_or_404(Productos, pk_producto=data["pk_producto"]);
    updated_inventario = get_object_or_404(Inventario, id_producto=data["pk_producto"])

    updated_inventario.stock_actual = data["stock_actual"]
    updated_inventario.stock_sugerido = data["stock_sugerido"] 

    # Modificar los siguientes 3 elementos para una clave foránea
    # Se actualiza la tabla inventarios
    updated_inventario.descripcion = data["descripcion"]
    updated_inventario.tipo = data["tipo_producto"]
    updated_inventario.fecha_actualizacion = data["fecha"]
    updated_inventario.save()
    # Se actualiza en la tabla producto
    producto.nombre = data["nombre"]
    producto.tipo_producto = data["tipo_producto"]
    producto.unidad_medida = data["unidad_medida"]
    producto.descripcion = data["descripcion"]
    producto.costo = data["costo"]
    producto.precio = data["precio"]
    producto.save()

    return JsonResponse({'message': 'Producto actualizado con éxito'}, status=200)

# FUNCIONES PARA INVENTARIO
def Obtener_inventario(request, UserPk):
    data = Inventario.objects.filter(id_user_id=UserPk).select_related('id_producto').values(
        'id_producto_id',
        'fecha_actualizacion',
        'stock_actual',
        'stock_sugerido',
    )
    
    response = []
    for item in data:
        producto = Productos.objects.get(pk_producto=item['id_producto_id'])
        response.append({
            'id_producto': producto.pk_producto,
            'nombre': producto.nombre,
            'tipo_producto': producto.tipo_producto,
            'descripcion': producto.descripcion,
            'fecha_actualizacion': item['fecha_actualizacion'],
            'stock_actual': item['stock_actual'],
            'stock_sugerido': item['stock_sugerido'],
        })

    return JsonResponse(response, safe=False)

# FUNCIONES PARA COTIZACIONES
def get_cotizaciones(request, pk):
    cotizaciones = Cotizaciones.objects.filter(id_user=pk)
    name_user = Usuarios.objects.get(id=pk)

    response = []
    for item in cotizaciones:
        response.append({
            'id_detalle': item.id_coti,
            'usuario': name_user.nombre,
            'fecha_elaboracion': item.fecha_elaboracion,
            'iva': item.iva,
            'total': item.total,
            'status': item.status
        })

    return JsonResponse(response, safe=False)

def nueva_cotizacion(request, pk):
    data = json.loads(request.body)
    user = get_object_or_404(Usuarios, id=pk)

    requirements = ['id_user', 'fecha_elaboracion', 'iva', 'total', 'status' ]
    for item in requirements:
        if item not in data['cotizacion']:
            return JsonResponse(f'El dato *{item}* es requerido en la solicitud')

    nueva_cotizacion = Cotizaciones.objects.create(
        id_user = user,
        fecha_elaboracion = data['cotizacion']['fecha_elaboracion'],
        iva = data['cotizacion']['iva'],
        total = data['cotizacion']['total'],
        status = data['cotizacion']['status']
    )
    nueva_cotizacion.save()

    for item in data['detalles']:
        producto = Productos.objects.get(pk_producto=item['id_producto'])
        nueva_detalle = DetalleCotizaciones.objects.create(
            id_coti = nueva_cotizacion.id_coti,
            id_producto = producto,
            descripcion = producto.descripcion,
            unidad_medida = producto.unidad_medida,
            cantidad = item['cantidad'],
            precio_unitario = item['precio_unitario'],
            total = item['cantidad'] * item['precio_unitario']
        )
        nueva_detalle.save()

    return JsonResponse('Creado con éxito', safe=False, status=201)

def eliminar_cotizacion(request):
    data = json.loads(request.body)

    cotizacion = get_object_or_404(Cotizaciones, id_coti=data['id_coti'])
    detalle = DetalleCotizaciones.objects.filter(id_coti=data['id_coti'])

    cotizacion.delete()
    detalle.delete()
  

    return JsonResponse('eliminado con completo', safe=False)