import customtkinter as ctk
from controllers import TransactionController, MainController, ReportController
from views.components import (MetricCard, TransactionListItem, ChartGenerator, 
                              ToastNotification)
from utils import CurrencyFormatter, get_current_month_year, get_month_name
from typing import Optional

class DashboardView(ctk.CTkScrollableFrame):
    """View do Dashboard principal"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.transaction_controller = TransactionController()
        self.report_controller = ReportController()
        self.current_month, self.current_year = get_current_month_year()
        
        self.configure(fg_color='#F8F9FA')
        self.grid_columnconfigure(0, weight=1)
        
        self._create_widgets()
        self.load_data()
    
    def _create_widgets(self):
        """Cria os widgets da interface"""
        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        
        title = ctk.CTkLabel(header, 
                            text=f"Dashboard - {get_month_name(self.current_month)}/{self.current_year}",
                            font=('Segoe UI', 24, 'bold'))
        title.pack(side='left')
        
        # Botão atualizar
        refresh_btn = ctk.CTkButton(header, text="🔄 Atualizar", 
                                   command=self.load_data,
                                   width=120)
        refresh_btn.pack(side='right')
        
        # Cards de métricas
        metrics_frame = ctk.CTkFrame(self, fg_color='transparent')
        metrics_frame.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 20))
        metrics_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.income_card = MetricCard(metrics_frame, "Entradas", "R$ 0,00", "💰", "#27AE60")
        self.income_card.grid(row=0, column=0, padx=10, sticky='ew')
        
        self.expense_card = MetricCard(metrics_frame, "Saídas", "R$ 0,00", "💸", "#E74C3C")
        self.expense_card.grid(row=0, column=1, padx=10, sticky='ew')
        
        self.balance_card = MetricCard(metrics_frame, "Saldo", "R$ 0,00", "📊", "#2E86AB")
        self.balance_card.grid(row=0, column=2, padx=10, sticky='ew')
        
        # Gráfico de categorias
        chart_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        chart_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        chart_title = ctk.CTkLabel(chart_frame, text="Gastos por Categoria",
                                   font=('Segoe UI', 16, 'bold'))
        chart_title.pack(pady=15)
        
        self.chart_container = ctk.CTkFrame(chart_frame, fg_color='transparent')
        self.chart_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Transações recentes
        recent_frame = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        recent_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        recent_title = ctk.CTkLabel(recent_frame, text="Transações Recentes",
                                   font=('Segoe UI', 16, 'bold'))
        recent_title.pack(pady=15)
        
        self.transactions_container = ctk.CTkFrame(recent_frame, fg_color='transparent')
        self.transactions_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def load_data(self):
        """Carrega dados do dashboard"""
        try:
            # Métricas
            metrics = self.report_controller.get_dashboard_metrics(
                self.current_month, self.current_year
            )
            
            # Atualizar cards
            self.income_card.update_value(
                CurrencyFormatter.format(metrics['income']),
                f"{metrics['transaction_count']} transações"
            )
            
            variation = metrics['expense_variation']
            variation_text = f"{'↑' if variation > 0 else '↓'} {abs(variation):.1f}% vs mês anterior"
            
            self.expense_card.update_value(
                CurrencyFormatter.format(metrics['expenses']),
                variation_text
            )
            
            balance_color = '#27AE60' if metrics['balance'] >= 0 else '#E74C3C'
            self.balance_card.configure(fg_color=balance_color)
            self.balance_card.update_value(
                CurrencyFormatter.format(metrics['balance'])
            )
            
            # Gráfico de categorias
            self._load_chart()
            
            # Transações recentes
            self._load_recent_transactions()
            
        except Exception as e:
            print(f"Erro ao carregar dashboard: {e}")
    
    def _load_chart(self):
        """Carrega gráfico de categorias"""
        # Limpar container
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        try:
            data = self.report_controller.get_category_breakdown(
                self.current_month, self.current_year
            )
            
            if data:
                figure = ChartGenerator.create_pie_chart(data)
                chart_widget = ChartGenerator.embed_chart(self.chart_container, figure)
                chart_widget.pack(fill='both', expand=True)
            else:
                no_data = ctk.CTkLabel(self.chart_container, 
                                      text="Nenhum gasto registrado neste mês",
                                      font=('Segoe UI', 12),
                                      text_color='#7F8C8D')
                no_data.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar gráfico: {e}")
    
    def _load_recent_transactions(self):
        """Carrega transações recentes"""
        # Limpar container
        for widget in self.transactions_container.winfo_children():
            widget.destroy()
        
        try:
            transactions = self.transaction_controller.get_all_transactions(limit=5)
            
            if transactions:
                for trans in transactions:
                    trans_data = {
                        'id': trans.id,
                        'date': trans.transaction_date.strftime('%d/%m/%Y'),
                        'description': trans.description,
                        'category': trans.category.name if trans.category else 'Sem categoria',
                        'category_icon': trans.category.icon if trans.category else '📁',
                        'amount': trans.amount,
                        'type': trans.type if isinstance(trans.type, str) else (trans.type.value if trans.type else 'expense')
                    }
                    
                    item = TransactionListItem(self.transactions_container, trans_data)
                    item.pack(fill='x', pady=5)
            else:
                no_trans = ctk.CTkLabel(self.transactions_container,
                                       text="Nenhuma transação registrada",
                                       font=('Segoe UI', 12),
                                       text_color='#7F8C8D')
                no_trans.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar transações: {e}")
    
    def cleanup(self):
        """Limpa recursos"""
        self.transaction_controller.close()
        self.report_controller.close()
