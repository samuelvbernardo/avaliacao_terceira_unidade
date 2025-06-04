from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Paciente, Medico, Consulta, Perfil

# formset customizado para validar o campo 'tipo' no Perfil inline
class PerfilInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data.get('tipo'):
                raise ValidationError("O campo 'tipo' do Perfil é obrigatório.")

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    formset = PerfilInlineFormSet
    extra = 0  # para não mostrar formulários extras vazios

class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]

# registrando os modelos normais
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Consulta)

# registrando User com o UserAdmin customizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
