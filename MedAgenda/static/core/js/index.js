document.addEventListener("DOMContentLoaded", function() {
    // Busca dinâmica para médicos
    const formBuscaMedico = document.getElementById("form-busca-medico");
    if (formBuscaMedico) {
        formBuscaMedico.addEventListener("submit", function(e) {
            e.preventDefault();
            const termo = document.getElementById("campo-busca-medico").value;
            fetch(`/tabela-medicos/?q_medico=${encodeURIComponent(termo)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("tabela-medicos").innerHTML = data.html;
                });
        });
    }

    // Busca dinâmica para pacientes
    const formBuscaPaciente = document.getElementById("form-busca-paciente");
    if (formBuscaPaciente) {
        formBuscaPaciente.addEventListener("submit", function(e) {
            e.preventDefault();
            const termo = document.getElementById("campo-busca-paciente").value;
            fetch(`/tabela-pacientes/?q_paciente=${encodeURIComponent(termo)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("tabela-pacientes").innerHTML = data.html;
                });
        });
    }

    // Alerta automático
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 3000);

    // Script para preencher o modal de detalhes do médico
    document.querySelectorAll('.btn-detalhe-medico').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('modal-nome').textContent = btn.getAttribute('data-nome');
            document.getElementById('modal-usuario').textContent = btn.getAttribute('data-usuario');
            document.getElementById('modal-email').textContent = btn.getAttribute('data-email');
            document.getElementById('modal-especialidade').textContent = btn.getAttribute('data-especialidade');
            document.getElementById('modal-crm').textContent = btn.getAttribute('data-crm');
            document.getElementById('modal-telefone').textContent = btn.getAttribute('data-telefone') || '---';
            document.getElementById('modal-entrada').textContent = btn.getAttribute('data-entrada');
            document.getElementById('modal-ultimo-login').textContent = btn.getAttribute('data-ultimo-login');
        });
    });

    // Script para preencher o modal de detalhes do paciente
    document.querySelectorAll('.btn-detalhe-paciente').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('modal-usuario-paciente').textContent = btn.getAttribute('data-usuario');
            document.getElementById('modal-paciente-nome').textContent = btn.getAttribute('data-nome');
            document.getElementById('modal-paciente-email').textContent = btn.getAttribute('data-email');
            document.getElementById('modal-paciente-telefone').textContent = btn.getAttribute('data-telefone');
            document.getElementById('modal-paciente-idade').textContent = btn.getAttribute('data-idade');
            document.getElementById('modal-paciente-altura').textContent = btn.getAttribute('data-altura');
        });
    });
    
    // Script para preencher e configurar o modal de finalização de consulta
    var finalizarModal = document.getElementById('finalizarModal');
    if (finalizarModal) {
        finalizarModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var consultaId = button.getAttribute('data-consulta-id');
            var form = document.getElementById('finalizarForm');
            if (form && consultaId) {
                // Atualiza a action do formulário para enviar para a consulta correta
                form.action = `/consulta/${consultaId}/finalizar/`;
                // Limpa o campo de observações ao abrir o modal
                form.querySelector('#observacoes').value = '';
            }
        });
    }

    // Script para preencher e configurar o modal de cancelamento de consulta
    var modalCancelar = document.getElementById('modalCancelarConsulta');
    if (modalCancelar) {
        modalCancelar.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var consultaId = button.getAttribute('data-consulta-id');
            var form = document.getElementById('formCancelarConsulta');
            if (form && consultaId) {
                form.action = `/consulta/${consultaId}/excluir/`; // ajuste conforme sua URL de exclusão
            }
        });
    }
});