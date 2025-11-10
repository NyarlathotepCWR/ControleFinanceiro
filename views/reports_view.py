import customtkinter as ctk
from controllers import ReportController
from views.components import ChartGenerator
from utils import get_current_month_year, get_month_name
from datetime import datetime

class ReportsView(ctk.CTkScrollableFrame):
    """View de relatórios e análises"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.report_controller = ReportController()
        self.current_month, self.current_year = get_current_month_year()
        
        self.configure(fg_color='#F8F9FA')
        self.grid_columnconfigure(0, weight=1)
        
        self._create_widgets()
        self.load_reports()
    
    def _create_widgets(self):
        """Cria widgets da interface"""
        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        
        title = ctk.CTkLabel(header, text="Relatórios e Análises",
                            font=('Segoe UI', 24, 'bold'))
        title.pack(side='left')
        
        # Seletor de período
        period_frame = ctk.CTkFrame(header, fg_color='transparent')
        period_frame.pack(side='right')
        
        months = [get_month_name(i) for i in range(1, 13)]
        self.month_combo = ctk.CTkComboBox(period_frame, values=months, width=150)
        self.month_combo.set(get_month_name(self.current_month))
        self.month_combo.pack(side='left', padx=5)
        
        years = [str(y) for y in range(datetime.now().year - 2, datetime.now().year + 2)]
        self.year_combo = ctk.CTkComboBox(period_frame, values=years, width=100)
        self.year_combo.set(str(self.current_year))
        self.year_combo.pack(side='left', padx=5)
        
        update_btn = ctk.CTkButton(period_frame, text="🔄", width=40,
                                  command=self._update_period)
        update_btn.pack(side='left', padx=5)
        
        # Container de gráficos
        charts_container = ctk.CTkFrame(self, fg_color='transparent')
        charts_container.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 20))
        charts_container.grid_columnconfigure((0, 1), weight=1)
        
        # Gráfico de pizza - Categorias
        self.pie_frame = ctk.CTkFrame(charts_container, fg_color='white', corner_radius=10)
        self.pie_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        pie_title = ctk.CTkLabel(self.pie_frame, text="Gastos por Categoria",
                                font=('Segoe UI', 16, 'bold'))
        pie_title.pack(pady=15)
        
        self.pie_container = ctk.CTkFrame(self.pie_frame, fg_color='transparent', height=400)
        self.pie_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Gráfico de barras - Métodos de pagamento
        self.bar_frame = ctk.CTkFrame(charts_container, fg_color='white', corner_radius=10)
        self.bar_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        
        bar_title = ctk.CTkLabel(self.bar_frame, text="Métodos de Pagamento",
                                font=('Segoe UI', 16, 'bold'))
        bar_title.pack(pady=15)
        
        self.bar_container = ctk.CTkFrame(self.bar_frame, fg_color='transparent', height=400)
        self.bar_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Gráfico de evolução mensal
        self.evolution_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        self.evolution_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        evo_title = ctk.CTkLabel(self.evolution_frame, text="Evolução Mensal (Últimos 6 meses)",
                                font=('Segoe UI', 16, 'bold'))
        evo_title.pack(pady=15)
        
        self.evolution_container = ctk.CTkFrame(self.evolution_frame, fg_color='transparent')
        self.evolution_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Maiores despesas
        self.top_expenses_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        self.top_expenses_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        top_title = ctk.CTkLabel(self.top_expenses_frame, text="Maiores Despesas do Mês",
                                font=('Segoe UI', 16, 'bold'))
        top_title.pack(pady=15)
        
        self.top_container = ctk.CTkScrollableFrame(self.top_expenses_frame, 
                                                    fg_color='transparent',
                                                    height=200)
        self.top_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def _update_period(self):
        """Atualiza período selecionado"""
        month_name = self.month_combo.get()
        months = [get_month_name(i) for i in range(1, 13)]
        self.current_month = months.index(month_name) + 1
        self.current_year = int(self.year_combo.get())
        self.load_reports()
    
    def load_reports(self):
        """Carrega todos os relatórios"""
        self._load_category_pie()
        self._load_payment_method_bar()
        self._load_evolution()
        self._load_top_expenses()
    
    def _load_category_pie(self):
        """Carrega gráfico de pizza de categorias"""
        # Limpar
        for widget in self.pie_container.winfo_children():
            widget.destroy()
        
        try:
            data = self.report_controller.get_category_breakdown(
                self.current_month, self.current_year
            )
            
            if data:
                figure = ChartGenerator.create_pie_chart(data, "Distribuição por Categoria")
                chart = ChartGenerator.embed_chart(self.pie_container, figure)
                chart.pack(fill='both', expand=True)
            else:
                no_data = ctk.CTkLabel(self.pie_container, 
                                      text="Sem dados disponíveis",
                                      font=('Segoe UI', 12),
                                      text_color='#7F8C8D')
                no_data.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar gráfico de categorias: {e}")
    
    def _load_payment_method_bar(self):
        """Carrega gráfico de barras de métodos de pagamento"""
        # Limpar
        for widget in self.bar_container.winfo_children():
            widget.destroy()
        
        try:
            data = self.report_controller.get_payment_method_breakdown(
                self.current_month, self.current_year
            )
            
            if data:
                # Converter para formato do gráfico
                chart_data = [
                    {'name': item['method'], 'total': item['total'], 'color': '#2E86AB'}
                    for item in data
                ]
                
                figure = ChartGenerator.create_bar_chart(chart_data, "Por Método de Pagamento")
                chart = ChartGenerator.embed_chart(self.bar_container, figure)
                chart.pack(fill='both', expand=True)
            else:
                no_data = ctk.CTkLabel(self.bar_container,
                                      text="Sem dados disponíveis",
                                      font=('Segoe UI', 12),
                                      text_color='#7F8C8D')
                no_data.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar gráfico de métodos: {e}")
    
    def _load_evolution(self):
        """Carrega gráfico de evolução mensal"""
        # Limpar
        for widget in self.evolution_container.winfo_children():
            widget.destroy()
        
        try:
            data = self.report_controller.get_monthly_evolution(self.current_year, months=6)
            
            if data:
                figure = ChartGenerator.create_line_chart(data, "Evolução Mensal")
                chart = ChartGenerator.embed_chart(self.evolution_container, figure)
                chart.pack(fill='both', expand=True)
            else:
                no_data = ctk.CTkLabel(self.evolution_container,
                                      text="Sem dados disponíveis",
                                      font=('Segoe UI', 12),
                                      text_color='#7F8C8D')
                no_data.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar evolução: {e}")
    
    def _load_top_expenses(self):
        """Carrega maiores despesas"""
        # Limpar
        for widget in self.top_container.winfo_children():
            widget.destroy()
        
        try:
            expenses = self.report_controller.get_top_expenses(
                self.current_month, self.current_year, limit=10
            )
            
            if expenses:
                for idx, exp in enumerate(expenses, 1):
                    item_frame = ctk.CTkFrame(self.top_container, fg_color='#ECF0F1', 
                                             corner_radius=8)
                    item_frame.pack(fill='x', pady=5)
                    item_frame.grid_columnconfigure(1, weight=1)
                    
                    # Posição
                    pos_label = ctk.CTkLabel(item_frame, text=f"#{idx}",
                                            font=('Segoe UI', 14, 'bold'),
                                            width=50)
                    pos_label.grid(row=0, column=0, padx=10, pady=10)
                    
                    # Descrição
                    desc_label = ctk.CTkLabel(item_frame, text=exp['description'],
                                             font=('Segoe UI', 12),
                                             anchor='w')
                    desc_label.grid(row=0, column=1, sticky='w', padx=10, pady=10)
                    
                    # Categoria
                    cat_label = ctk.CTkLabel(item_frame, 
                                            text=exp.get('category_name', 'Sem categoria'),
                                            font=('Segoe UI', 10),
                                            text_color='#7F8C8D')
                    cat_label.grid(row=0, column=2, padx=10, pady=10)
                    
                    # Valor
                    from utils import CurrencyFormatter
                    value_label = ctk.CTkLabel(item_frame,
                                              text=CurrencyFormatter.format(exp['amount']),
                                              font=('Segoe UI', 14, 'bold'),
                                              text_color='#E74C3C')
                    value_label.grid(row=0, column=3, padx=10, pady=10)
            else:
                no_data = ctk.CTkLabel(self.top_container,
                                      text="Sem despesas registradas",
                                      font=('Segoe UI', 12),
                                      text_color='#7F8C8D')
                no_data.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar top despesas: {e}")
    
    def cleanup(self):
        """Limpa recursos"""
        self.report_controller.close()
