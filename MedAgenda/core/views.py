from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Consulta, Medico, Paciente, User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = "core/pages/login.html"

def logout_view(request):
    logout(request)
    return redirect('login')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = ''  # Será definido dinamicamente

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        perfil = user.perfil

        # Se for médico e não tiver cadastro completo
        if perfil.tipo == 'medico' and not hasattr(user, 'medico'):
            return redirect('completar_cadastro_medico')
        # Se for paciente e não tiver cadastro completo
        if perfil.tipo == 'paciente' and not hasattr(user, 'paciente'):
            return redirect('completar_cadastro_paciente')
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        user = self.request.user
        perfil = user.perfil
        if perfil.tipo == 'medico':
            return ['core/pages/perfil/medico/home_medico.html']
        elif perfil.tipo == 'paciente':
            return ['core/pages/perfil/paciente/home_paciente.html']
        elif perfil.tipo == 'admin':
            return ['core/pages/perfil/administrador/home_admin.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'medico'):
            context['nome_usuario'] = user.medico.nome
            context['medico'] = user.medico
        elif hasattr(user, 'paciente'):
            context['nome_usuario'] = user.paciente.nome
            context['paciente'] = user.paciente
        else:
            context['nome_usuario'] = user.get_full_name() or user.username
        return context

class CompletarCadastroMedicoView(LoginRequiredMixin, View):
    template_name = 'core/pages/perfil/medico/completar_cadastro_medico.html'

    def get(self, request):
        if hasattr(request.user, 'medico'):
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        if hasattr(request.user, 'medico'):
            return redirect('home')
        nome = request.POST.get('nome')
        especialidade = request.POST.get('especialidade')
        crm = request.POST.get('crm')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        Medico.objects.create(
            user=request.user,
            nome=nome,
            especialidade=especialidade,
            crm=crm,
            telefone=telefone,
            email=email
        )
        return redirect('home')
    
class MedicoUpdateView(LoginRequiredMixin, View):
    template_name = 'core/pages/perfil/medico/editar_medico.html'

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        medico = Medico.objects.get(pk=pk, user=request.user)  # Garante que é o médico do usuário logado
        return render(request, self.template_name, {'medico': medico})

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        medico = Medico.objects.get(pk=pk, user=request.user)
        medico.nome = request.POST.get('nome')
        medico.especialidade = request.POST.get('especialidade')
        medico.crm = request.POST.get('crm')
        medico.telefone = request.POST.get('telefone')
        medico.email = request.POST.get('email')
        medico.save()
        messages.success(request, "Alterações salvas com sucesso!")
        return redirect('editar_medico', pk=medico.pk)
    
class MedicoListView(ListView):
    model = Medico
    template_name = "core/pages/perfil/administrador/listar_medicos.html"
    context_object_name = "medicos"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q_medico", "")
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) |
                Q(email__icontains=q) |
                Q(especialidade__icontains=q) |
                Q(crm__icontains=q)
            )
        return queryset


        
class CompletarCadastroPacienteView(LoginRequiredMixin, View):
    template_name = 'core/pages/perfil/paciente/completar_cadastro_paciente.html'

    def get(self, request):
        if hasattr(request.user, 'paciente'):
            return redirect('home')
        return render(request, self.template_name)

    def post(self, request):
        if hasattr(request.user, 'paciente'):
            return redirect('home')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        idade = request.POST.get('idade')
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        Paciente.objects.create(
            user=request.user,
            nome=nome,
            email=email,
            telefone=telefone,
            idade=idade,
            peso=peso,
            altura=altura
        )
        return redirect('home')
    
class PacienteUpdateView(LoginRequiredMixin, View):
    template_name = 'core/pages/perfil/paciente/editar_paciente.html'

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        paciente = Paciente.objects.get(pk=pk, user=request.user)  # Garante que é o paciente do usuário logado
        return render(request, self.template_name, {'paciente': paciente})
    
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        paciente = Paciente.objects.get(pk=pk, user=request.user)
        paciente.nome = request.POST.get('nome')
        paciente.email = request.POST.get('email')
        paciente.telefone = request.POST.get('telefone')
        paciente.idade = request.POST.get('idade') or None
        peso = request.POST.get('peso')
        paciente.peso = float(peso) if peso not in [None, '', 'None'] else None
        paciente.altura = request.POST.get('altura') or None
        paciente.save()
        messages.success(request, "Alterações salvas com sucesso!")
        return redirect('editar_paciente', pk=paciente.pk)
    
class PacienteListView(ListView):
    model = Paciente
    template_name = "core/pages/perfil/administrador/listar_pacientes.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q_paciente", "")
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) |
                Q(email__icontains=q) |
                Q(telefone__icontains=q)
            )
        return queryset
    
class ConsultaCreateView(CreateView):
    model = Consulta
    fields = ['medico', 'data', 'horario', 'observacoes']
    template_name = 'core/pages/perfil/paciente/agendar_consultas.html'
    success_url = reverse_lazy('agendar_consultas')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['medico'].queryset = Medico.objects.all()
        return form

    def form_valid(self, form):
        paciente = Paciente.objects.get(user=self.request.user)
        form.instance.paciente = paciente
        form.instance.status = 'A'
        messages.success(self.request, "Agendamento concluido.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicos'] = Medico.objects.all()
        context['paciente'] = Paciente.objects.get(user=self.request.user)
        context['consultas'] = Consulta.objects.filter(paciente=context['paciente']).order_by('-data', '-horario')
        return context
        
class ConsultaFinalizarView(UpdateView):
    model = Consulta
    fields = ['observacoes']
    template_name = 'core/pages/perfil/medico/finalizar_consulta.html'
    success_url = reverse_lazy('consultas_medico')

    def form_valid(self, form):
        form.instance.status = 'R'  # Realizada
        messages.success(self.request, "Consulta finalizada com sucesso!")
        return super().form_valid(form)
    
class ConsultaListView(ListView):
    model = Consulta
    context_object_name = "consultas"
    paginate_by = 8

    def get_template_names(self):
        user = self.request.user
        if user.is_superuser:
            return ["core/pages/perfil/administrador/historico_consultas_admin.html"]
        elif hasattr(user, 'medico'):
            return ["core/pages/perfil/medico/historico_consultas_medico.html"]
        elif hasattr(user, 'paciente'):
            return ["core/pages/perfil/paciente/historico_consultas_paciente.html"]

    def get_queryset(self):
        user = self.request.user
        perfil = getattr(user, 'perfil', None)
        queryset = Consulta.objects.all().order_by("-data", "-horario")
        if perfil:
            if perfil.tipo == 'medico' and hasattr(user, 'medico'):
                queryset = queryset.filter(medico=user.medico)
            elif perfil.tipo == 'paciente' and hasattr(user, 'paciente'):
                queryset = queryset.filter(paciente=user.paciente)
            # admin vê todas as consultas
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'medico'):
            context['medico'] = user.medico
        elif hasattr(user, 'paciente'):
            context['paciente'] = user.paciente
        return context
    
@method_decorator(login_required, name='dispatch')
class AvaliarConsultaView(View):
    def post(self, request, pk):
        consulta = Consulta.objects.get(pk=pk)
        # Garante que só o paciente da consulta pode avaliar
        if hasattr(request.user, 'paciente') and consulta.paciente == request.user.paciente:
            avaliacao = request.POST.get('avaliacao')
            consulta.avaliacao = avaliacao
            consulta.save()
            messages.success(request, "Avaliação registrada com sucesso!")
        else:
            messages.error(request, "Você não pode avaliar esta consulta.")
        return redirect('historico')
        
class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = "core/pages/perfil/paciente/cancelar_consulta.html"
    success_url = reverse_lazy("agendar_consultas")

class ConsultasAgendadasMedicoView(ListView):
    model = Consulta
    context_object_name = "consultas"
    template_name = "core/pages/perfil/medico/consultas_medico.html"
    paginate_by = 8


class ConsultasAgendadasAdminView(ListView):
    model = Consulta
    template_name = 'core/pages/perfil/administrador/consultas_agendadas.html'
    context_object_name = 'consultas'

    def get_queryset(self):
        queryset = Consulta.objects.filter(status='A').order_by('data', 'horario')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(paciente__nome__icontains=q) |
                Q(medico__nome__icontains=q) |
                Q(medico__especialidade__icontains=q)
            )
        return queryset

    
class MedicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medico
    template_name = "core/pages/perfil/medico/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_medicos")

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = "core/pages/perfil/paciente/confirmar_exclusao.html"
    success_url = reverse_lazy("listar_pacientes")

class BuscarConsultasView(View):
    def get(self, request):
        termo = request.GET.get("q", "")
        consultas = Consulta.objects.all().order_by("-data", "-horario")
        if termo:
            consultas = consultas.filter(
                Q(paciente__nome__icontains=termo) |
                Q(medico__nome__icontains=termo) |
                Q(medico__especialidade__icontains=termo)
            )
        html = render_to_string("core/partials/tabela_consultas.html", {"consultas": consultas})
        return JsonResponse({"html": html})

class BuscarMedicosView(ListView):
    model = Medico
    template_name = "core/partials/tabela_medicos.html"
    context_object_name = "medicos"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q_medico", "")
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) |
                Q(email__icontains=q) |
                Q(especialidade__icontains=q) |
                Q(crm__icontains=q)
            )
        return queryset

    def render_to_response(self, context):
        html = render_to_string(self.template_name, context, request=self.request)
        return JsonResponse({"html": html})

class BuscarPacientesView(ListView):
    model = Paciente
    template_name = "core/pages/perfil/administrador/partials/tabela_pacientes.html"
    context_object_name = "pacientes"

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q_paciente", "")
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) |
                Q(email__icontains=q) |
                Q(telefone__icontains=q)
            )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        html = render_to_string(self.template_name, context, request=self.request)
        return JsonResponse({"html": html})