import customtkinter as ctk
from controllers import BudgetController, MainController
from views.components import BudgetProgressBar, ToastNotification, CurrencyEntry
from utils import get_current_month_year, get_month_name

class BudgetsView(ctk.CTkFrame):
    """View de gerenciamento de orçamentos"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.budget_controller = BudgetController()
        self.main_controller = MainController()
        self.current_month, self.current_year = get_current_month_year()
        
        self.configure(fg_color='#F8F9FA')
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self.load_budgets()
    
    def _create_widgets(self):
        """Cria widgets da interface"""
        # Painel de configuração de orçamentos
        config_panel = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        config_panel.grid(row=0, column=0, sticky='nsew', padx=(20, 10), pady=20)
        
        # Título
        title = ctk.CTkLabel(config_panel, text="Configurar Orçamentos",
                            font=('Segoe UI', 18, 'bold'))
        title.pack(pady=20)
        
        # Seletor de período
        period_frame = ctk.CTkFrame(config_panel, fg_color='transparent')
        period_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        period_label = ctk.CTkLabel(period_frame, text="Período:",
                                   font=('Segoe UI', 12, 'bold'))
        period_label.pack(anchor='w', pady=(0, 5))
        
        period_select = ctk.CTkFrame(period_frame, fg_color='transparent')
        period_select.pack(fill='x')
        
        months = [get_month_name(i) for i in range(1, 13)]
        self.month_combo = ctk.CTkComboBox(period_select, values=months, width=150)
        self.month_combo.set(get_month_name(self.current_month))
        self.month_combo.pack(side='left', padx=(0, 10))
        
        from datetime import datetime
        years = [str(y) for y in range(datetime.now().year - 1, datetime.now().year + 3)]
        self.year_combo = ctk.CTkComboBox(period_select, values=years, width=100)
        self.year_combo.set(str(self.current_year))
        self.year_combo.pack(side='left')
        
        # Formulário de orçamento
        form_container = ctk.CTkScrollableFrame(config_panel, fg_color='transparent')
        form_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Selecionar categoria
        cat_label = ctk.CTkLabel(form_container, text="Categoria:",
                                font=('Segoe UI', 12, 'bold'))
        cat_label.pack(anchor='w', pady=(10, 5))
        
        self.category_combo = ctk.CTkComboBox(form_container, values=["Carregando..."])
        self.category_combo.pack(fill='x', pady=(0, 10))
        
        # Valor do orçamento
        amount_label = ctk.CTkLabel(form_container, text="Valor Orçado:",
                                   font=('Segoe UI', 12, 'bold'))
        amount_label.pack(anchor='w', pady=(10, 5))
        
        self.amount_entry = CurrencyEntry(form_container, placeholder_text="R$ 0,00")
        self.amount_entry.pack(fill='x', pady=(0, 10))
        
        # Limite de alerta
        alert_label = ctk.CTkLabel(form_container, text="Alerta ao atingir (%):",
                                  font=('Segoe UI', 12, 'bold'))
        alert_label.pack(anchor='w', pady=(10, 5))
        
        self.alert_slider = ctk.CTkSlider(form_container, from_=50, to=100, number_of_steps=10)
        self.alert_slider.set(80)
        self.alert_slider.pack(fill='x', pady=(0, 5))
        
        self.alert_value_label = ctk.CTkLabel(form_container, text="80%",
                                             font=('Segoe UI', 11))
        self.alert_value_label.pack(anchor='w')
        
        self.alert_slider.configure(command=self._update_alert_label)
        
        # Botões
        button_frame = ctk.CTkFrame(config_panel, fg_color='transparent')
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        save_btn = ctk.CTkButton(button_frame, text="💾 Salvar Orçamento",
                                command=self.save_budget,
                                fg_color='#27AE60',
                                hover_color='#229954')
        save_btn.pack(fill='x', pady=5)
        
        refresh_btn = ctk.CTkButton(button_frame, text="🔄 Atualizar",
                                   command=self.load_budgets,
                                   fg_color='#2E86AB',
                                   hover_color='#1F5F7A')
        refresh_btn.pack(fill='x', pady=5)
        
        # Painel de status dos orçamentos
        status_panel = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        status_panel.grid(row=0, column=1, sticky='nsew', padx=(10, 20), pady=20)
        
        # Título do status
        status_title = ctk.CTkLabel(status_panel, 
                                   text=f"Status - {get_month_name(self.current_month)}/{self.current_year}",
                                   font=('Segoe UI', 18, 'bold'))
        status_title.pack(pady=20)
        
        # Container scrollable para orçamentos
        self.budgets_container = ctk.CTkScrollableFrame(status_panel, fg_color='transparent')
        self.budgets_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def _update_alert_label(self, value):
        """Atualiza label do slider de alerta"""
        self.alert_value_label.configure(text=f"{int(value)}%")
    
    def load_budgets(self):
        """Carrega orçamentos do período"""
        # Atualizar período
        months = [get_month_name(i) for i in range(1, 13)]
        self.current_month = months.index(self.month_combo.get()) + 1
        self.current_year = int(self.year_combo.get())
        
        # Carregar categorias
        self._load_categories()
        
        # Limpar container
        for widget in self.budgets_container.winfo_children():
            widget.destroy()
        
        try:
            budgets = self.budget_controller.get_all_budget_status(
                self.current_month, self.current_year
            )
            
            if budgets:
                for budget in budgets:
                    progress = BudgetProgressBar(
                        self.budgets_container,
                        category_name=budget['category_name'],
                        budgeted=budget['budgeted'],
                        spent=budget['spent'],
                        icon=budget.get('category_icon', '📊'),
                        color=budget.get('category_color', '#2E86AB')
                    )
                    progress.pack(fill='x', pady=10)
                    
                    # Alerta se excedeu limite
                    if budget['alert']:
                        alert_frame = ctk.CTkFrame(progress, fg_color='#E74C3C', corner_radius=5)
                        alert_frame.pack(fill='x', padx=15, pady=(0, 10))
                        
                        alert_label = ctk.CTkLabel(alert_frame, 
                                                  text=f"⚠️ Atenção! {budget['percentage']:.1f}% do orçamento utilizado",
                                                  text_color='white',
                                                  font=('Segoe UI', 10, 'bold'))
                        alert_label.pack(pady=5)
            else:
                no_budget = ctk.CTkLabel(self.budgets_container,
                                        text="Nenhum orçamento configurado para este período",
                                        font=('Segoe UI', 12),
                                        text_color='#7F8C8D')
                no_budget.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar orçamentos: {e}")
    
    def _load_categories(self):
        """Carrega categorias disponíveis"""
        try:
            categories = self.main_controller.get_all_categories()
            cat_names = [f"{cat.icon} {cat.name}" for cat in categories]
            self.category_combo.configure(values=cat_names)
            if cat_names:
                self.category_combo.set(cat_names[0])
            self.categories = categories
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
    
    def save_budget(self):
        """Salva configuração de orçamento"""
        try:
            # Obter dados
            amount = self.amount_entry.get_value()
            alert_threshold = self.alert_slider.get() / 100
            
            # Validações
            if amount <= 0:
                ToastNotification(self, "Valor deve ser maior que zero", type='error')
                return
            
            # Encontrar categoria selecionada
            selected_text = self.category_combo.get()
            category_id = None
            
            for cat in self.categories:
                if f"{cat.icon} {cat.name}" == selected_text:
                    category_id = cat.id
                    break
            
            if not category_id:
                ToastNotification(self, "Selecione uma categoria válida", type='error')
                return
            
            # Obter período
            months = [get_month_name(i) for i in range(1, 13)]
            month = months.index(self.month_combo.get()) + 1
            year = int(self.year_combo.get())
            
            # Salvar
            self.budget_controller.add_budget(
                category_id=category_id,
                amount=amount,
                month=month,
                year=year,
                alert_threshold=alert_threshold
            )
            
            ToastNotification(self, "Orçamento salvo com sucesso!", type='success')
            self.load_budgets()
            
        except Exception as e:
            ToastNotification(self, f"Erro ao salvar: {str(e)}", type='error')
            print(f"Erro detalhado: {e}")
    
    def cleanup(self):
        """Limpa recursos"""
        self.budget_controller.close()
        self.main_controller.close()
