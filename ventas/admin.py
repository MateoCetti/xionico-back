from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(VentaCabecera)
admin.site.register(Vendedor)
admin.site.register(VentaDetalle)
admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Producto)