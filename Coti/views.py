import json
from django.conf import settings
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Productos, Cotizaciones, DetalleCotizaciones, Usuarios, Inventario
import weasyprint
from django.template.loader import render_to_string
import os
from datetime import datetime

# views.py
def pdf_generator(request, pk, CotiId):
    # Datos de ejemplo para la cotización
    UserCotizacion = Cotizaciones.objects.filter(id_user=pk)
    Cotizacion = UserCotizacion.get(id_coti=CotiId)
    DetalleCotizacion = DetalleCotizaciones.objects.filter(id_coti=CotiId)

    #extraer el mes de la fecha para el titulo de la cotizacion
    def extraer_mes(fecha, formato="numero"):
        # Convertir la fecha de cadena a objeto datetime
        fecha = datetime.strptime(str(fecha), "%Y-%m-%d")
        
        # Obtener el mes en número o en nombre según el formato solicitado
        if formato == "nombre":
            return fecha.strftime("%B")  # Mes como nombre completo, por ejemplo, "October"
        elif formato == "nombre_corto":
            return fecha.strftime("%b")  # Mes como nombre abreviado, por ejemplo, "Oct"
        else:
            return fecha.month  # Mes como número, por ejemplo, 10

    comentario = Cotizacion.comentarios
    sub_total = Cotizacion.sub_total
    iva = Cotizacion.iva
    descuento = 0
    total = Cotizacion.total
    cliente= Cotizacion.cliente
    contacto= Cotizacion.contacto
    telefono= Cotizacion.telefono
    domicilio= Cotizacion.domicilio
    fecha= Cotizacion.fecha_elaboracion
    mes= extraer_mes(Cotizacion.fecha_elaboracion)
    NoCoti=CotiId

    Coti_response = []
    for item in DetalleCotizacion:
        Coti_response.append({
            'partida': item.id_detalle,
            'descripcion': item.descripcion,
            'unidad_medida': item.unidad_medida,
            'cantidad': item.cantidad,
            'precio_unitario': item.precio_unitario,
            'importe': item.total
            })

    # Generar la URL completa para el archivo CSS
    css_path = os.path.join(settings.STATIC_ROOT, 'pdf/styleTemplate.css')

    # Crear la URL completa para el logo
    logo_url = request.build_absolute_uri("static/pdf/Logo_360.png")  # Cambia según la ruta real de tu imagen en /static

    # Rendering el HTML con contexto de datos
    html_string = render_to_string(
        'CotiTemplate.html', {
            'productos': Coti_response,
            'comentario': comentario,
            'sub_total': sub_total,
            'iva': iva,
            'descuento': descuento,
            'total': total,
            'cliente': cliente,
            'contacto': contacto,
            'telefono': telefono,
            'domicilio': domicilio,
            'fecha': fecha,
            'NoCoti': NoCoti,
            'mes': mes
        }
    )

    # Generar el archivo PDF
    pdf_file = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[weasyprint.CSS(css_path)])

    # Crear la respuesta HTTP para descargar el PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cotizacion.pdf"'
    
    return response

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
def lista_productos(request, pk):
    if request.method == 'GET':
        return Obtener_Productos(request, pk)
    elif request.method == 'POST':
        return Crear_producto(request, pk)
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
        return eliminar_cotizacion(request, pk)
    else:  
        return HttpResponse("Metodo Invalido", status=405)
     
def detalle_cotizaciones(request, CotiId):
    if request.method == 'GET':
        detalles = list(DetalleCotizaciones.objects.filter(id_coti=CotiId).values())

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

    response={ 
        'message': 'Usuario actualizado con éxito',
        'usuario': {
            'id': usuario.id,
            'empresa': usuario.empresa,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': usuario.rol,
            }
    }

    return JsonResponse(response, status=200, safe=False) 

def get_usuario(request, pk):
    usuario = get_object_or_404(Usuarios, id=pk).usuario_dict()
    
    return JsonResponse(usuario, safe=False)

def delete_usuario(request, pk):
    usuario = get_object_or_404(Usuarios, id=pk)
    name_user = usuario.nombre
    usuario.delete()

    return JsonResponse(f'usuario {name_user} eliminado con éxito', safe=False, status=200)

# FUNCIONES PARA PRODUCTOS
def Obtener_Productos(request, pk):
    productos = list(Productos.objects.filter(id_user_id=pk).values())

    return JsonResponse(productos, safe=False)

def Crear_producto(request, pk):
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
            'stock_actual': data['stock_actual'],
            'fecha_actualizacion': data['fecha_actualizacion']
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
        return JsonResponse('Producto eliminado o no encontrado', status=400, safe=False)

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

    response = {
        "message": 'Producto actualizado con éxito',
        "data": {
            'pk_producto': producto.pk_producto,   
            'nombre': producto.nombre,
            'tipo_producto': producto.tipo_producto,
            'unidad_medida': producto.unidad_medida,
            'descripcion': producto.descripcion,
            'costo': producto.costo,
            'precio': producto.precio,
            'stock_actual': updated_inventario.stock_actual,
            'stock_sugerido': updated_inventario.stock_sugerido,
            'fecha_actualizacion': updated_inventario.fecha_actualizacion,
        }
    }
    return JsonResponse(response, status=200, safe=False)

# FUNCIONES PARA INVENTARIO
def Obtener_inventario(request, UserPk):
    data = Inventario.objects.filter(id_user_id=UserPk).select_related('id_producto').values(
        'id_inventario',
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
            'id_inventario': item['id_inventario']
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
            'cliente': item.cliente,
            'contacto': item.contacto,
            'telefono': item.telefono,
            'domicilio': item.domicilio,
            'sub_total': item.sub_total,
            'iva': item.iva,
            'total': item.total,
            'status': item.status
        })

    return JsonResponse(response, safe=False)

def nueva_cotizacion(request, pk):
    data = json.loads(request.body)
    user = get_object_or_404(Usuarios, id=pk)

    requirements = [ 'fecha_elaboracion', 'iva', 'total', 'status' ]
    for item in requirements:
        if item not in data['cotizacion']:
            return JsonResponse(f'El dato *{item}* es requerido en la solicitud', safe=False)

    response_full = {
        "cotizacion": {},
        "detalles": []
        }
    
    nueva_cotizacion = Cotizaciones.objects.create(
        id_user = user,
        fecha_elaboracion = data['cotizacion']['fecha_elaboracion'],
        status = data["cotizacion"]["status"],
        cliente = data["cotizacion"]["cliente"],
        contacto = data["cotizacion"]["contacto"],
        telefono = data["cotizacion"]["telefono"],
        domicilio = data["cotizacion"]["domicilio"],
        iva = data['cotizacion']['iva'],
        total = data['cotizacion']['total'],
        comentarios = data['cotizacion']['comentarios']
    )
    nueva_cotizacion.save()
    response_full['cotizacion']={
        'id_detalle': nueva_cotizacion.id_coti,
        'usuario': user.nombre,
        'fecha_elaboracion': nueva_cotizacion.fecha_elaboracion,
        'cliente': nueva_cotizacion.cliente,
        'contacto': nueva_cotizacion.contacto, 
        'telefono': nueva_cotizacion.telefono,
        'domicilio': nueva_cotizacion.domicilio,
        'sub_total': nueva_cotizacion.sub_total,
        'iva': nueva_cotizacion.iva,
        'total': nueva_cotizacion.total,
        'status': nueva_cotizacion.status
    }

    for item in data['detalles']:
        producto = get_object_or_404(Productos, pk_producto=item['id_producto'])
        nuevo_detalle = DetalleCotizaciones.objects.create(
            id_coti = nueva_cotizacion.id_coti,
            id_producto = producto,
            descripcion = producto.descripcion,
            unidad_medida = producto.unidad_medida,
            cantidad = item['cantidad'],
            precio_unitario = item['precio_unitario'],
            total = item['cantidad'] * item['precio_unitario']
        )
        nuevo_detalle.save()
        response_full['detalles'].append({
            'id_detalle': nuevo_detalle.id_detalle,
            'id_coti': nuevo_detalle.id_coti,
            'producto': producto.nombre,
            'descripcion': nuevo_detalle.descripcion,
            'unidad_medida': nuevo_detalle.unidad_medida,
            'cantidad': nuevo_detalle.cantidad,
            'precio_unitario': nuevo_detalle.precio_unitario,
            'total': nuevo_detalle.total
        })


    return JsonResponse(response_full, safe=False, status=201)

def eliminar_cotizacion(request, pk):
    data = json.loads(request.body)

    cotizacion = get_object_or_404(Cotizaciones, id_coti=data['id_coti'])
    detalle = DetalleCotizaciones.objects.filter(id_coti=data['id_coti'])

    cotizacion.delete()
    detalle.delete()
  
    return JsonResponse('eliminado completo', safe=False)

def actualizar_cotizacion(request, pk):
    data = json.loads(request.body)
    nueva_cotizacion = Cotizaciones.objects.get(id_coti=data['cotizacion']['id_coti'])

    nueva_cotizacion.fecha_elaboracion = data['cotizacion']['fecha_elaboracion']
    nueva_cotizacion.cliente = data['cotizacion']['cliente']
    nueva_cotizacion.contacto = data['cotizacion']['contacto']
    nueva_cotizacion.telefono = data['cotizacion']['telefono']
    nueva_cotizacion.domicilio = data['cotizacion']['domicilio']
    nueva_cotizacion.sub_total = data['cotizacion']['sub_total']
    nueva_cotizacion.iva = data['cotizacion']['iva']
    nueva_cotizacion.total = data['cotizacion']['total']
    nueva_cotizacion.status = data['cotizacion']['status']
    nueva_cotizacion.save()

     # Actualizar el stock si la cotización fue aceptada
    if data['cotizacion']['status'] == 'aceptada':
        for item in data['detalles']:
            producto = get_object_or_404(Inventario, id_producto=item['id_producto'])
            producto.stock_actual -= item['cantidad']
            producto.save()

    for item in data['detalles']:
        nuevos_detalles = DetalleCotizaciones.objects.filter(id_coti=data['cotizacion']['id_coti'])

        for detalle in nuevos_detalles:
            detalle.descripcion = item['descripcion']
            detalle.unidad_medida = item['unidad_medida']
            detalle.cantidad = item['cantidad']
            detalle.precio_unitario = item['precio_unitario']
            detalle.total = item['cantidad'] * item['precio_unitario']

            detalle.save()
        

    return JsonResponse('actualizado completo', safe=False)