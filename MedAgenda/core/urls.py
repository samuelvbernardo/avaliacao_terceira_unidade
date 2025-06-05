from django.urls import path
from . import views
from .views import (
    HomeView,
    CompletarCadastroMedicoView,
    CompletarCadastroPacienteView,
    ConsultaCreateView,
    ConsultaFinalizarView,
    ConsultaListView,
    ConsultaDeleteView,
    BuscarConsultasView,
    BuscarMedicosView,
    BuscarPacientesView,
    ConsultasAgendadasMedicoView,
    AvaliarConsultaView, ConsultasAgendadasAdminView
)

urlpatterns = [
    path("", views.CustomLoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("home", HomeView.as_view(), name="home"),
    path('completar-cadastro/medico/', CompletarCadastroMedicoView.as_view(), name='completar_cadastro_medico'),
    path('medico/<int:pk>/editar/', views.MedicoUpdateView.as_view(), name='editar_medico'),
    path('medicos/', views.MedicoListView.as_view(), name='listar_medicos'),
    path('completar-cadastro/paciente/', CompletarCadastroPacienteView.as_view(), name='completar_cadastro_paciente'),
    path('paciente/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='editar_paciente'),
    path('pacientes/', views.PacienteListView.as_view(), name='listar_pacientes'),
    path("consulta/", ConsultaCreateView.as_view(), name="agendar_consultas"),
    path("consulta/<int:pk>/finalizar/", ConsultaFinalizarView.as_view(), name="finalizar_consulta"),
    path("historico", ConsultaListView.as_view(), name="historico"),
    path("consulta/<int:pk>/excluir/", ConsultaDeleteView.as_view(), name="cancelar_consulta"),
    path("buscar-consultas/", BuscarConsultasView.as_view(), name="buscar_consultas"),
    path('tabela-medicos/', BuscarMedicosView.as_view(), name='tabela_medicos'),
    path('tabela-pacientes/', BuscarPacientesView.as_view(), name='tabela_pacientes'),
    path('consultas/<int:pk>/avaliar/', AvaliarConsultaView.as_view(), name='avaliar_consulta'),
    path('consultas/', ConsultasAgendadasMedicoView.as_view(), name='consultas_medico'),
    path('consultas-admin/', ConsultasAgendadasAdminView.as_view(), name='consultas_admin'),
]