from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Form

from .models import User, Pedido, Produto, ItemPedido, Endereco


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('saldo', 'cpf')}),
    )
    list_display = UserAdmin.list_display + ('saldo',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'score', 'estoque', 'listado')


@admin.register(Pedido)
class PedidooAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'status', 'cliente', 'subtotal', 'total')

# criar snippets parecidos com o de cima para cada model do banco de dados.
