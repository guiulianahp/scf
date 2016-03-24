from django.contrib import admin
from sistema_sfc.apps.scf.models import Producto, Cliente, Cotizacion, Factura, Producto_has_cotizacion, Prospecto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Cotizacion)
admin.site.register(Factura)
admin.site.register(Producto_has_cotizacion)
admin.site.register(Prospecto)
