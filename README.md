# MedAgenda  
**Sistema de Gerenciamento de Consultas Médicas**

---

## 1. Introdução e Visão Geral

**MedAgenda** é uma plataforma web desenvolvida em Django para facilitar o gerenciamento de consultas em clínicas médicas, integrando médicos, pacientes e administradores em um único sistema. O objetivo é organizar o fluxo de agendamentos, histórico e informações de cada perfil, promovendo segurança e praticidade.

---

## 2. Principais Funcionalidades

### **Administrador**
- Responsável por popular o sistema (cadastro de usuários via Django Admin)
- Visualiza todos os médicos e pacientes cadastrados e suas informações detalhadas
- Acompanha todas as consultas agendadas na clínica
- Tem acesso ao histórico completo de consultas da clínica

### **Médico**
- Ao fazer login pela primeira vez, caso não tenha cadastro completo, é redirecionado para preencher seus dados
- Após o cadastro, pode acessar a home do sistema
- Pode editar seu perfil a qualquer momento
- Visualiza suas consultas agendadas e os detalhes dos pacientes atendidos
- Finaliza consultas após o atendimento
- Tem acesso ao seu histórico de consultas realizadas

### **Paciente**
- Ao fazer login pela primeira vez, caso não tenha cadastro completo, é redirecionado para preencher seus dados
- Após o cadastro, pode acessar a home do sistema
- Pode editar seu perfil a qualquer momento
- Agenda novas consultas com médicos disponíveis
- Visualiza suas consultas agendadas e os detalhes do médico responsável
- Pode cancelar consultas agendadas
- Tem acesso ao seu histórico de consultas

---

## 3. Arquitetura do Projeto

- O projeto utiliza um **template base principal**, que centraliza todos os links de estilos, scripts e componentes comuns.
- A partir desse base, foram criados dois arquivos base herdados:  
  - Um exclusivo para o **administrador**
  - Outro compartilhado para os **usuários médicos e pacientes**
- A tela **home** é definida dinamicamente após o login, por meio da `HomeView`, que redireciona cada usuário para a interface adequada conforme seu perfil.
- Os **templates** estão organizados em pastas separadas dentro de `perfil`, agrupando as telas de **administrador**, **médico** e **paciente**.
- Essa estrutura facilita a manutenção, a reutilização de código e garante que cada perfil tenha acesso apenas às funcionalidades e informações pertinentes.
- A partir da home, cada usuário pode navegar pelas funcionalidades disponíveis para o seu perfil, tornando o sistema intuitivo e seguro.

---

## 4. Tecnologias Utilizadas

- **Backend:** Django (Python)
- **Frontend:** HTML, Bootstrap, JavaScript (modais, AJAX)
- **Banco de Dados:** SQLite (desenvolvimento) e PostgreSQL (banco final)
- **Admin Django** customizado

---

## 5. Diferenciais Técnicos

- **Controle de acesso** com autenticação e perfis
- **Componentização de templates** (partials para tabelas, navegação, rodapé)
- **Modais reutilizáveis** para detalhes de médicos e pacientes
- **Busca dinâmica** sem recarregar a página
- **Mensagens de feedback** para ações do usuário
- **Código JavaScript centralizado** para interações

---

## 6. Pontos de Atenção e Melhorias

- Validação de dados mais robusta
- Tratamento de exceções nas views
- Internacionalização das mensagens
- Testes automatizados
- Entre outros

---

## 7. Conclusão

O projeto está pronto para ser expandido e adaptado conforme as necessidades de uso.

---

**Dúvidas ou sugestões? Estou à disposição!**
