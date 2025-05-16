from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome","email","senha")

admin.site.register(Usuario, UsuarioAdmin)