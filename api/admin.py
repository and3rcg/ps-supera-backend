from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass

# criar snippets parecidos com o de cima para cada model do banco de dados.
