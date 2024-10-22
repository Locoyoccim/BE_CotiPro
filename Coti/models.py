from django.db import models

# Create your models here.
from django.db import models

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True) 
    empresa = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)

    class Meta:
        db_table = 'usuarios'

    def usuarios_dict(self):
        return{
            'empresa': self.empresa,
            'nombre': self.nombre,
            'email':  self.email,
            'password': self.password,
            'rol': self.rol
        }

class Productos(models.Model):
    id_user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)  # Relación con Usuario
    nombre = models.CharField(max_length=255)
    tipo_producto = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50)
    descripcion = models.TextField(null=True, blank=True)  # `descripcion` puede ser nulo
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'productos'

    def producto_dict(self):
        return {
            'id_user': self.id_user,
            'nombre': self.nombre,
            'tipo_producto': self.tipo_producto,
            'unidad_medida': self.unidad_medida,
            'descripcion': self.descripcion,
            'costo': self.costo,
            'precio': self.costo
        }

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)  # Cambia User si usas otro modelo de usuario
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    fecha_actualizacion = models.DateField()
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    stock_actual = models.IntegerField()
    stock_sugerido = models.IntegerField()

    class Meta:
        db_table = 'inventario'

class Cotizaciones(models.Model):
    id_coti = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Usuarios, on_delete=models.CASCADE)  # Relación con el modelo de usuarios
    fecha_elaboracion = models.DateField()
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'cotizaciones'

class DetalleCotizaciones(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_coti = models.ForeignKey(Cotizaciones, on_delete=models.CASCADE)  # Relación con la tabla cotizaciones
    id_producto = models.ForeignKey(Productos, on_delete=models.SET_NULL, null=True)  # Relación con la tabla productos
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detallecotizaciones'