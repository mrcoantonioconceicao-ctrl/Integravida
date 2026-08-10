# Orion Abordagem v2.0

## 📋 Visão Geral

**Orion Abordagem** é um sistema profissional de integração social para cadastro, avaliação e encaminhamento de pessoas em situação de vulnerabilidade. Desenvolvido especificamente para a realidade de Blumenau/SC, conecta a triagem social à rede de acolhimento local.

**Slogan:** "Reconectando pessoas à vida com dignidade"

**Contexto:** Sistema operacional para assistência social em Blumenau, com encaminhamentos automatizados para órgãos municipais reais (Abordagem Social, Centro POP, CAPS, CREAS, DPCAMI, Abrigo Municipal).

## 🎯 Funcionalidades

### Sistema de Autenticação
- Login com credenciais
- Demo: `usuario / 123456` ou `admin / admin123`
- Sessão persistente no navegador

### Dashboard Gerencial
- Total de atendimentos registrados
- Atendimentos do dia
- Motivo principal mais recorrente
- Listagem dos últimos 5 atendimentos
- Acesso rápido a todas as funcionalidades

### Novo Atendimento
- Formulário completo com campos:
  - Nome completo, idade, gênero
  - Cidade/localização
  - Motivo (7 opções predefinidas)
  - Descrição detalhada da situação
  - Responsável pelo atendimento
- Validação de campos obrigatórios
- Salvamento automático no servidor, com backup local no navegador

### Gerenciamento de Atendimentos
- Tabela com todos os atendimentos registrados
- Visualização detalhada
- Encaminhamentos inteligentes por motivo
- Deleção de registros
- PDF individual para cada atendimento

### Sistema de Relatórios
- **PDF Individual:** Relatório completo de um atendimento
- **Resumo:** Estatísticas gerais de atendimentos
- **Estatísticas:** Análise por gênero, idade média, motivos

### Configurações
- Informações do sistema
- Exportação de dados (JSON)
- Importação de dados (JSON)
- Backup e restauração completa

## 🛠️ Tecnologias

- HTML5
- CSS3 (Moderno, responsivo)
- JavaScript Vanilla (Sem dependências externas)
- jsPDF (Geração de PDF)
- Python HTTP server (API de persistência)
- Arquivo JSON local do servidor (persistência dos atendimentos)
- localStorage (backup local e sessão do usuário)

## 🚀 Como Usar

### Acesso ao Sistema
1. Acesse http://localhost:5000
2. Use credenciais: `usuario / 123456`
3. Clique em "Acessar Sistema"

### Fluxo Principal
1. **Novo Atendimento:** Preencha o formulário com todos os dados
2. **Salvar:** Clique em "Salvar Atendimento"
3. **Visualizar:** Acesse em "Atendimentos" para ver o histórico
4. **Gerar PDF:** Clique em "Ver" e depois em "Gerar PDF"
5. **Exportar:** Use "Configurações" para fazer backup

## 📊 Encaminhamentos Automáticos

O sistema oferece encaminhamentos inteligentes baseado no motivo:

- **Dependência Química:** Comunidade terapêutica especializada
- **Depressão:** CAPS ou psicólogo
- **Doença Mental:** Hospital especializado
- **Desemprego:** Centro de profissionalização
- **Violência Doméstica:** Delegacia e casas de acolhimento
- **Falta de Moradia:** Casa de passagem ou centro de apoio
- **Outros:** Órgão competente específico

## 💾 Armazenamento de Dados

- Os atendimentos são salvos no servidor em `integravida_data.json`
- Os dados permanecem disponíveis após logout, novo login e reinício do servidor
- O navegador mantém um backup local para recuperação durante uma indisponibilidade do servidor
- Nenhum dado é enviado a servidores externos
- Possibilidade de exportar em JSON para backup

## 🎨 Design e UX

- Interface moderna e profissional
- Cores corporativas: Vermelho (#c1121f) e Azul-escuro (#1a1a2e)
- Design responsivo (mobile, tablet, desktop)
- Navegação intuitiva com sidebar
- Ícones para melhor visualização
- Feedback visual (alertas, toasts)

## 📱 Responsividade

- Desktop: Sidebar fixa, layout em 2 colunas
- Tablet: Adaptação automática
- Mobile: Sidebar horizontal, layout em 1 coluna

## 🔐 Segurança

- Senhas hardcoded (apenas para demo)
- Recomenda-se implementar backend com autenticação real
- Dados sensíveis não são coletados
- Conformidade com LGPD (dados armazenados localmente)

## 📈 Estatísticas

O sistema coleta e analisa:
- Total de atendimentos
- Atendimentos por dia
- Distribuição por gênero
- Idade média dos atendidos
- Motivos mais recorrentes
- Encaminhamentos realizados

## 🎁 Funcionalidades Premium (Sugeridas para V3)

- Autenticação com backend (Node.js/Python)
- Banco de dados relacional (PostgreSQL)
- Multi-usuário com permissões
- Integração com mapas (localização de instituições)
- Notificações por email
- Dashboard com gráficos avançados
- API REST para integração
- Sincronização em nuvem
- Importação de dados (CSV/Excel)

## 👨‍💻 Desenvolvedor

**Marco Antônio Conceição**  
Empresa: **NEXT**  
Versão: **2.0**  
Licença: **MIT**

## 📝 Notas

- Sistema totalmente funcional pronto para apresentação
- Interface intuitiva para usuários sem conhecimento técnico
- Dados persistem no armazenamento do servidor
- Exportação/Importação para backup e migração
- Pronto para ser deployado em Replit
