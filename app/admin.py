from django.contrib import admin
from .models import Usuario
from .models import Produto, Categoria

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome","email","senha")

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nomeProduto","descricaoProduto","precoProduto","imagemProduto", "qtdeEstoque","categoriaProduto")

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Produto, ProdutoAdmin)