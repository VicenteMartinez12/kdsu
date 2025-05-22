from django.contrib import admin
from .models import Documento, Factura, Factura_detalle, Factura_archivo, Desglose

admin.site.register(Documento)
admin.site.register(Factura)
admin.site.register(Factura_detalle)
admin.site.register(Factura_archivo)
admin.site.register(Desglose)
