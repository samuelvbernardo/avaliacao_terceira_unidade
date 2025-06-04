from django import forms
from .models import Medico, Paciente

class CompletarCadastroMedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nome', 'especialidade', 'crm', 'telefone', 'email']

class CompletarCadastroPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'email', 'telefone', 'idade', 'peso', 'altura']