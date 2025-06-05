from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Paciente, Medico, Consulta, Perfil

# Registrando os modelos no Django Admin
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Consulta)

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)