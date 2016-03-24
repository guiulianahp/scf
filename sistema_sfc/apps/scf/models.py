from django.db import models

# Create your models here.

#-----------------------------------------------------#
# 					TABLA PRODUCTOS
#-----------------------------------------------------#
class Producto(models.Model):
    nombre 		 = models.CharField(max_length = 100)
    descripcion  = models.CharField(max_length = 200)
    precio_tp	 = models.FloatField()
    precio_tg	 = models.FloatField()

    def __str__(self):
        return '%s %s %d %d' % (self.nombre, self.descripcion, self.precio_tp, self.precio_tg)
  

#-----------------------------------------------------#
# 					TABLA CLIENTES
#-----------------------------------------------------#
class Cliente(models.Model):
    rif			 = models.CharField(max_length  = 100)
    nombre 		 = models.CharField(max_length  = 100)
    telefono     = models.CharField(max_length  = 20)
    correo	 	 = models.CharField(max_length  = 200)
    direccion	 = models.CharField(max_length  = 250)

    def __str__(self):
        return '%s %s %s %s %s' % (self.rif, self.nombre, self.telefono, self.correo, self.direccion)


#-----------------------------------------------------#
# 					TABLA COTIZACION
#-----------------------------------------------------#
class Cotizacion(models.Model):
    
    fecha		 		   = models.DateTimeField()
    cliente_identificacion = models.ForeignKey(Cliente)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.fecha, self.cliente_identificacion)

    
#-----------------------------------------------------#
# 					TABLA PRODUCTOS_COTIZACION
#-----------------------------------------------------#
class Producto_has_cotizacion(models.Model):
    producto_id_producto 	 = models.ForeignKey(Producto)
    cotizacion_id_cotizacion = models.ForeignKey(Cotizacion)
    cantidad     			 = models.IntegerField()
    precio                   = models.FloatField()
    ganancia	 	 		 = models.FloatField()
    talla                    = models.CharField(max_length = 20, default = 'S')
    

    def __str__(self):
        return '%s %s %s %s %s %s' % (self.producto_id_producto, self.cotizacion_id_cotizacion, self.cantidad, self.precio, self.ganancia, self.talla)
   

#-----------------------------------------------------#
# 					TABLA FACTURA
#-----------------------------------------------------#
class Factura(models.Model):
    cotizacion_id_cotizacion = models.ForeignKey(Cotizacion)
    fecha 		 			 = models.DateTimeField()
    num_factura              = models.IntegerField()

    def __str__(self):
        return '%s %s %s' % (self.cotizacion_id_cotizacion, self.fecha, self.num_factura)
   

#-----------------------------------------------------#
#					TABLA PROSPECTOS
#-----------------------------------------------------#
class Prospecto(models.Model):
    nombre 		= models.CharField(max_length = 100)
    telefono 	= models.CharField(max_length = 20)
    correo		= models.CharField(max_length = 200)

    def  __str__(self):
        return '%s %s %s' % (self.nombre, self.telefono, self.correo)

#-----------------------------------------------------#
#                   TABLA OBSERVACIONES
#-----------------------------------------------------#
class Observacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion)
    descripcion   = models.CharField(max_length = 200)

    def  __str__(self):
        return '%s %s' % (self.cotizacion, self.descripcion)

#-----------------------------------------------------#
#          TABLA OBSERVACIONES POR DEFECTO
#-----------------------------------------------------#
class Observacion_por_defecto(models.Model):
    descripcion   = models.CharField(max_length = 200)

    def  __str__(self):
        return '%s' % (self.descripcion)