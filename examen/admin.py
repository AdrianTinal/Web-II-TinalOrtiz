from django.contrib import admin

from .models import Boleto, Evento, Localidad

admin.site.register(Boleto)
admin.site.register(Evento)
admin.site.register(Localidad)