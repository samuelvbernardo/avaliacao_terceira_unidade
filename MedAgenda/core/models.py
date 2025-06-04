from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    TIPOS = [
        ('admin', 'Administrador'),
        ('paciente', 'Paciente'),
        ('medico', 'Médico'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_display()}"

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    idade = models.PositiveIntegerField(blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # Ex: 120.50 kg
    altura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # Ex: 1.75 m

    def __str__(self):
        return self.nome

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=40)
    especialidade = models.CharField(max_length=30)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"
    
class Consulta(models.Model):
    STATUS_CHOICES = [
        ('A', 'Agendada'),
        ('R', 'Realizada'),
        ('C', 'Cancelada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')                    
    avaliacao = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=[(i, f"{i} Estrela{'s' if i > 1 else ''}") for i in range(1, 6)]
    )
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def tipo(self):
        return self.medico.especialidade

    def __str__(self):
        return f"{self.tipo} - {self.paciente} com {self.medico} em {self.data} às {self.horario}"