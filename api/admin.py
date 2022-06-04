from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Form

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('saldo', 'cpf')}),
    )
    list_display = UserAdmin.list_display + ('saldo',)

# criar snippets parecidos com o de cima para cada model do banco de dados.
