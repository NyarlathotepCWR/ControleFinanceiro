# Controle Financeiro Pessoal

Aplicação completa de controle de gastos mensais desenvolvida em Python com interface moderna e intuitiva.

## Funcionalidades

### Principais
- **Dashboard Interativo**: Métricas em tempo real, gráficos e resumos
- **Gerenciamento de Transações**: CRUD completo com validações
- **Categorias Personalizáveis**: Organize seus gastos por categoria
- **Orçamentos Inteligentes**: Defina metas e receba alertas
- **Relatórios Detalhados**: Análises gráficas e comparativos
- **Persistência de Dados**: SQLite com SQLAlchemy ORM

### Recursos Avançados
- Múltiplos métodos de pagamento
- Sistema de tags para transações
- Comparação com mês anterior
- Gráficos de evolução temporal
- Alertas de orçamento excedido
- Validações em tempo real

## Instalação

### Opção 1: Executável (Recomendado para usuários finais)

#### Windows
1. Execute `build.bat` para criar o executável
2. O arquivo será criado em `dist\ControleFinanceiro.exe`
3. Copie o executável para qualquer pasta
4. Execute diretamente clicando duas vezes

**Nota:** O executável é standalone e não precisa de Python instalado.

### Opção 2: Instalação Completa (Para desenvolvedores)

#### Windows
1. Execute `install.bat` (instala Python e dependências)
2. Execute `run.bat` para iniciar a aplicação

#### Linux/Mac
1. Execute `chmod +x install.sh run.sh`
2. Execute `./install.sh`
3. Execute `./run.sh` para iniciar

### Opção 3: Manual

#### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

#### Passos

1. Clone ou baixe o repositório

2. Instale as dependências:
```powershell
pip install -r requirements.txt
```

3. Execute a aplicação:
```powershell
python main.py
```

## Estrutura do Projeto

```
financial_app/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── models/                 # Modelos de dados (ORM)
│   ├── database.py
│   ├── categories.py
│   ├── transactions.py
│   └── budgets.py
├── controllers/            # Lógica de negócio
│   ├── main_controller.py
│   ├── transaction_controller.py
│   ├── report_controller.py
│   └── budget_controller.py
├── views/                  # Interface gráfica
│   ├── main_window.py
│   ├── dashboard_view.py
│   ├── transactions_view.py
│   ├── reports_view.py
│   ├── budgets_view.py
│   └── components/        # Componentes reutilizáveis
│       ├── charts.py
│       ├── forms.py
│       └── widgets.py
└── utils/                 # Utilitários
    ├── validators.py
    ├── formatters.py
    └── helpers.py
```

## Uso

### Adicionar Transação
1. Acesse a aba "Transações"
2. Preencha o formulário (descrição, valor, categoria, data)
3. Selecione o tipo (Despesa/Receita) e método de pagamento
4. Clique em "Salvar"

### Configurar Orçamento
1. Acesse a aba "Orçamentos"
2. Selecione o período e categoria
3. Defina o valor orçado e limite de alerta
4. Clique em "Salvar Orçamento"

### Visualizar Relatórios
1. Acesse a aba "Relatórios"
2. Selecione o período desejado
3. Visualize gráficos e análises

## Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **CustomTkinter**: Interface gráfica moderna
- **SQLAlchemy**: ORM para persistência
- **Matplotlib**: Geração de gráficos
- **Pydantic**: Validação de dados
- **tkcalendar**: Seletor de datas

## Banco de Dados

O banco SQLite é criado automaticamente na primeira execução (`financial_data.db`).

### Categorias Padrão
- Alimentação 🍽️
- Transporte 🚗
- Moradia 🏠
- Saúde ⚕️
- Educação 📚
- Lazer 🎮
- Vestuário 👔
- Salário 💰
- Outros 📦

## Validações

- Valores devem ser positivos
- Descrições são obrigatórias
- Datas no formato DD/MM/AAAA
- Categorias devem existir

## Paleta de Cores

- **Primary**: #2E86AB (Azul)
- **Success**: #27AE60 (Verde)
- **Warning**: #F39C12 (Laranja)
- **Danger**: #E74C3C (Vermelho)
- **Background**: #F8F9FA (Cinza Claro)

## Desenvolvimento Futuro

- [ ] Exportação para PDF/Excel
- [ ] Backup automático
- [ ] Modo escuro
- [ ] Gráficos interativos
- [ ] Sincronização multi-dispositivo
- [ ] Importação de extratos bancários
- [ ] Categorias personalizadas com ícones

## Licença

Este projeto é de código aberto para fins educacionais.

## Autor

Desenvolvido como sistema completo de controle financeiro pessoal.

## Suporte

Para problemas ou sugestões, verifique se todas as dependências estão instaladas corretamente.
