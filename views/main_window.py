import customtkinter as ctk
from views.dashboard_view import DashboardView
from views.transactions_view import TransactionsView
from views.reports_view import ReportsView
from views.budgets_view import BudgetsView

class MainWindow(ctk.CTk):
    """Janela principal da aplicação"""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("Controle Financeiro Pessoal")
        self.geometry("1400x800")
        
        # Tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Layout principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Menu lateral
        self._create_sidebar()
        
        # Container de conteúdo
        self.content_container = ctk.CTkFrame(self, fg_color='transparent')
        self.content_container.grid(row=0, column=1, sticky='nsew')
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Visualizações
        self.views = {}
        self.current_view = None
        
        # Mostrar dashboard por padrão
        self.show_view('dashboard')
    
    def _create_sidebar(self):
        """Cria menu lateral de navegação"""
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color='#2C3E50')
        sidebar.grid(row=0, column=0, sticky='nsew')
        sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Título
        logo_frame = ctk.CTkFrame(sidebar, fg_color='#1F2D3D')
        logo_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        logo_label = ctk.CTkLabel(logo_frame, text="💰 Finanças", 
                                 font=('Segoe UI', 24, 'bold'),
                                 text_color='white')
        logo_label.pack(pady=20)
        
        subtitle = ctk.CTkLabel(logo_frame, text="Controle Financeiro",
                               font=('Segoe UI', 12),
                               text_color='#BDC3C7')
        subtitle.pack(pady=(0, 15))
        
        # Botões de navegação
        self.nav_buttons = {}
        
        nav_items = [
            ('dashboard', '📊 Dashboard', 1),
            ('transactions', '💳 Transações', 2),
            ('budgets', '🎯 Orçamentos', 3),
            ('reports', '📈 Relatórios', 4),
        ]
        
        for view_id, text, row in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                font=('Segoe UI', 14),
                height=50,
                corner_radius=0,
                fg_color='transparent',
                hover_color='#34495E',
                anchor='w',
                command=lambda v=view_id: self.show_view(v)
            )
            btn.grid(row=row, column=0, sticky='ew', padx=10, pady=5)
            self.nav_buttons[view_id] = btn
        
        # Informações do rodapé
        footer = ctk.CTkFrame(sidebar, fg_color='#1F2D3D')
        footer.grid(row=7, column=0, sticky='ew')
        
        version_label = ctk.CTkLabel(footer, text="Versão 1.0.0",
                                    font=('Segoe UI', 10),
                                    text_color='#7F8C8D')
        version_label.pack(pady=10)
    
    def show_view(self, view_id: str):
        """Exibe uma visualização específica"""
        # Ocultar visualização atual
        if self.current_view:
            if hasattr(self.current_view, 'cleanup'):
                self.current_view.cleanup()
            self.current_view.grid_forget()
        
        # Resetar cores dos botões
        for btn in self.nav_buttons.values():
            btn.configure(fg_color='transparent')
        
        # Destacar botão ativo
        if view_id in self.nav_buttons:
            self.nav_buttons[view_id].configure(fg_color='#34495E')
        
        # Criar ou mostrar visualização
        if view_id not in self.views:
            if view_id == 'dashboard':
                self.views[view_id] = DashboardView(self.content_container)
            elif view_id == 'transactions':
                self.views[view_id] = TransactionsView(self.content_container)
            elif view_id == 'reports':
                self.views[view_id] = ReportsView(self.content_container)
            elif view_id == 'budgets':
                self.views[view_id] = BudgetsView(self.content_container)
        
        # Mostrar visualização
        if view_id in self.views:
            self.current_view = self.views[view_id]
            self.current_view.grid(row=0, column=0, sticky='nsew')
            
            # Recarregar dados se tiver método load_data
            if hasattr(self.current_view, 'load_data'):
                self.current_view.load_data()
            elif hasattr(self.current_view, 'load_reports'):
                self.current_view.load_reports()
            elif hasattr(self.current_view, 'load_budgets'):
                self.current_view.load_budgets()
    
    def run(self):
        """Inicia a aplicação"""
        self.mainloop()
