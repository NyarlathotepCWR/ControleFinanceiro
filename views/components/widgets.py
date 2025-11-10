import customtkinter as ctk
from typing import Callable, Optional

class MetricCard(ctk.CTkFrame):
    """Card de métrica para dashboard"""
    
    def __init__(self, master, title: str, value: str, icon: str = "📊", 
                 color: str = "#2E86AB", subtitle: str = ""):
        super().__init__(master, fg_color=color, corner_radius=10)
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        
        # Ícone e título
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        
        icon_label = ctk.CTkLabel(header_frame, text=icon, font=('Segoe UI', 24))
        icon_label.pack(side='left')
        
        title_label = ctk.CTkLabel(header_frame, text=title, 
                                   font=('Segoe UI', 12), 
                                   text_color='white')
        title_label.pack(side='left', padx=(10, 0))
        
        # Valor principal
        self.value_label = ctk.CTkLabel(self, text=value, 
                                       font=('Segoe UI', 28, 'bold'),
                                       text_color='white')
        self.value_label.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        # Subtítulo (opcional)
        if subtitle:
            self.subtitle_label = ctk.CTkLabel(self, text=subtitle,
                                              font=('Segoe UI', 10),
                                              text_color='white')
            self.subtitle_label.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 15))
        else:
            # Espaçamento final
            spacer = ctk.CTkFrame(self, fg_color="transparent", height=15)
            spacer.grid(row=2, column=0)
    
    def update_value(self, value: str, subtitle: str = ""):
        """Atualiza valor do card"""
        self.value_label.configure(text=value)
        if hasattr(self, 'subtitle_label') and subtitle:
            self.subtitle_label.configure(text=subtitle)

class TransactionListItem(ctk.CTkFrame):
    """Item de lista de transação"""
    
    def __init__(self, master, transaction_data: dict, 
                 on_edit: Optional[Callable] = None,
                 on_delete: Optional[Callable] = None):
        super().__init__(master, fg_color='white', corner_radius=8)
        
        self.transaction_data = transaction_data
        self.on_edit = on_edit
        self.on_delete = on_delete
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        
        # Data
        date_label = ctk.CTkLabel(self, text=transaction_data.get('date', ''),
                                 font=('Segoe UI', 10),
                                 text_color='#7F8C8D',
                                 width=80)
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        # Descrição e categoria
        desc_frame = ctk.CTkFrame(self, fg_color='transparent')
        desc_frame.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
        
        desc_label = ctk.CTkLabel(desc_frame, 
                                 text=transaction_data.get('description', ''),
                                 font=('Segoe UI', 12, 'bold'),
                                 anchor='w')
        desc_label.pack(anchor='w')
        
        cat_label = ctk.CTkLabel(desc_frame,
                                text=f"{transaction_data.get('category_icon', '📁')} {transaction_data.get('category', '')}",
                                font=('Segoe UI', 10),
                                text_color='#95A5A6',
                                anchor='w')
        cat_label.pack(anchor='w')
        
        # Valor
        amount = transaction_data.get('amount', 0)
        trans_type = transaction_data.get('type', 'expense')
        
        color = '#27AE60' if trans_type == 'income' else '#E74C3C'
        prefix = '+' if trans_type == 'income' else '-'
        
        amount_label = ctk.CTkLabel(self, 
                                   text=f"{prefix} R$ {amount:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                                   font=('Segoe UI', 14, 'bold'),
                                   text_color=color,
                                   width=120)
        amount_label.grid(row=0, column=2, padx=10, pady=10)
        
        # Botões de ação
        if on_edit or on_delete:
            action_frame = ctk.CTkFrame(self, fg_color='transparent')
            action_frame.grid(row=0, column=3, padx=10, pady=10)
            
            if on_edit:
                edit_btn = ctk.CTkButton(action_frame, text="✏️", width=40,
                                        command=lambda: on_edit(transaction_data))
                edit_btn.pack(side='left', padx=2)
            
            if on_delete:
                delete_btn = ctk.CTkButton(action_frame, text="🗑️", width=40,
                                          fg_color='#E74C3C',
                                          hover_color='#C0392B',
                                          command=lambda: on_delete(transaction_data))
                delete_btn.pack(side='left', padx=2)

class BudgetProgressBar(ctk.CTkFrame):
    """Barra de progresso para orçamento"""
    
    def __init__(self, master, category_name: str, budgeted: float, 
                 spent: float, icon: str = "📊", color: str = "#2E86AB"):
        super().__init__(master, fg_color='white', corner_radius=8)
        
        self.budgeted = budgeted
        self.spent = spent
        self.percentage = (spent / budgeted * 100) if budgeted > 0 else 0
        
        # Layout
        self.grid_columnconfigure(1, weight=1)
        
        # Cabeçalho
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.grid(row=0, column=0, columnspan=2, sticky='ew', padx=15, pady=(15, 5))
        
        name_label = ctk.CTkLabel(header, text=f"{icon} {category_name}",
                                 font=('Segoe UI', 12, 'bold'),
                                 anchor='w')
        name_label.pack(side='left')
        
        percent_label = ctk.CTkLabel(header, text=f"{self.percentage:.1f}%",
                                    font=('Segoe UI', 11, 'bold'),
                                    text_color=color)
        percent_label.pack(side='right')
        
        # Barra de progresso
        progress_bg = ctk.CTkFrame(self, fg_color='#ECF0F1', height=20, corner_radius=10)
        progress_bg.grid(row=1, column=0, columnspan=2, sticky='ew', padx=15, pady=5)
        progress_bg.grid_propagate(False)
        
        # Determinar cor da barra
        if self.percentage >= 100:
            bar_color = '#E74C3C'
        elif self.percentage >= 80:
            bar_color = '#F39C12'
        else:
            bar_color = color
        
        width_percent = min(self.percentage / 100, 1.0)
        progress_bar = ctk.CTkFrame(progress_bg, fg_color=bar_color, corner_radius=10)
        progress_bar.place(relx=0, rely=0, relheight=1, relwidth=width_percent)
        
        # Valores
        values_frame = ctk.CTkFrame(self, fg_color='transparent')
        values_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=15, pady=(5, 15))
        
        spent_label = ctk.CTkLabel(values_frame, 
                                  text=f"Gasto: R$ {spent:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                                  font=('Segoe UI', 10),
                                  text_color='#7F8C8D')
        spent_label.pack(side='left')
        
        remaining = budgeted - spent
        remaining_label = ctk.CTkLabel(values_frame,
                                      text=f"Restante: R$ {remaining:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                                      font=('Segoe UI', 10),
                                      text_color='#7F8C8D')
        remaining_label.pack(side='right')
