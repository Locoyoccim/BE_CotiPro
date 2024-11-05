# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cotizaciones(models.Model):
    id_coti = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_user')
    fecha_elaboracion = models.DateField()
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    cliente = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    domicilio = models.CharField(max_length=255)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comentarios = models.TextField(blank=True, null=True)  # Nuevo campo opcional

    class Meta:
        managed = False
        db_table = 'cotizaciones'


class DetalleCotizaciones(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    id_coti = models.IntegerField()
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detallecotizaciones'

    def detalle_dict(self):
        return{
            'id_detalle': self.id_detalle,
            'id_coti': self.id_coti,
            'id_producto': self.id_producto,
            'descripcion': self.descripcion,
            'unidad_medida': self.unidad_medida,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'total': self.total
        }


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_user')
    id_producto = models.ForeignKey('Productos', models.DO_NOTHING, db_column='id_producto')
    fecha_actualizacion = models.DateField()
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    stock_actual = models.IntegerField()
    stock_sugerido = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventario'


class Productos(models.Model):
    id_user = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_user')
    pk_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    tipo_producto = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'productos'

    def producto_dict(self):
        return{
            'id_user': self.id_user,
            'pk_producto': self.pk_producto,
            'nombre': self.nombre,
            'tipo_producto': self.tipo_producto,
            'unidad_medida': self.unidad_medida,
            'descripcion': self.descripcion,
            'costo': self.costo,
            'precio': self.precio
        }


class Usuarios(models.Model):
    empresa = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'usuarios'

    def usuario_dict(self):
        return{ 
            'empresa': self.empresa,
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
            'rol': self.rol
        }