import customtkinter as ctk
from controllers import TransactionController, MainController
from models import TransactionType, PaymentMethod
from views.components import (DatePickerEntry, CurrencyEntry, CategoryComboBox, 
                              FormField, ToastNotification, TransactionListItem)
from datetime import datetime
from typing import Optional

class TransactionsView(ctk.CTkFrame):
    """View de gerenciamento de transações"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.transaction_controller = TransactionController()
        self.main_controller = MainController()
        self.categories = []
        self.editing_id: Optional[int] = None
        
        self.configure(fg_color='#F8F9FA')
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        self._create_widgets()
        self.load_categories()
        self.load_transactions()
    
    def _create_widgets(self):
        """Cria widgets da interface"""
        # Painel de formulário
        form_panel = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        form_panel.grid(row=0, column=0, sticky='nsew', padx=(20, 10), pady=20)
        
        # Título do formulário
        form_title = ctk.CTkLabel(form_panel, text="Nova Transação",
                                 font=('Segoe UI', 18, 'bold'))
        form_title.pack(pady=20)
        
        # Container do formulário
        form_container = ctk.CTkScrollableFrame(form_panel, fg_color='transparent')
        form_container.pack(fill='both', expand=True, padx=20)
        
        # Campo: Descrição
        self.description_field = FormField(form_container, "Descrição", ctk.CTkEntry,
                                          placeholder_text="Ex: Supermercado")
        self.description_field.pack(fill='x', pady=10)
        
        # Campo: Valor
        self.amount_field = FormField(form_container, "Valor", CurrencyEntry,
                                     placeholder_text="R$ 0,00")
        self.amount_field.pack(fill='x', pady=10)
        
        # Campo: Categoria
        cat_label = ctk.CTkLabel(form_container, text="Categoria", anchor='w')
        cat_label.pack(fill='x', pady=(10, 5))
        
        self.category_combo = CategoryComboBox(form_container, [])
        self.category_combo.pack(fill='x', pady=(0, 10))
        
        # Campo: Data
        date_label = ctk.CTkLabel(form_container, text="Data", anchor='w')
        date_label.pack(fill='x', pady=(10, 5))
        
        self.date_entry = DatePickerEntry(form_container)
        self.date_entry.pack(fill='x', pady=(0, 10))
        
        # Campo: Tipo de transação
        type_label = ctk.CTkLabel(form_container, text="Tipo", anchor='w')
        type_label.pack(fill='x', pady=(10, 5))
        
        self.type_combo = ctk.CTkComboBox(form_container, 
                                         values=['Despesa', 'Receita', 'Transferência'])
        self.type_combo.set('Despesa')
        self.type_combo.pack(fill='x', pady=(0, 10))
        
        # Campo: Método de pagamento
        method_label = ctk.CTkLabel(form_container, text="Método de Pagamento", anchor='w')
        method_label.pack(fill='x', pady=(10, 5))
        
        payment_methods = [method.value for method in PaymentMethod]
        self.method_combo = ctk.CTkComboBox(form_container, values=payment_methods)
        self.method_combo.set(payment_methods[0])
        self.method_combo.pack(fill='x', pady=(0, 10))
        
        # Campo: Notas
        notes_label = ctk.CTkLabel(form_container, text="Notas (opcional)", anchor='w')
        notes_label.pack(fill='x', pady=(10, 5))
        
        self.notes_entry = ctk.CTkTextbox(form_container, height=80)
        self.notes_entry.pack(fill='x', pady=(0, 10))
        
        # Botões
        button_frame = ctk.CTkFrame(form_panel, fg_color='transparent')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.save_btn = ctk.CTkButton(button_frame, text="💾 Salvar",
                                     command=self.save_transaction,
                                     fg_color='#27AE60',
                                     hover_color='#229954')
        self.save_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        self.clear_btn = ctk.CTkButton(button_frame, text="🗑️ Limpar",
                                      command=self.clear_form,
                                      fg_color='#7F8C8D',
                                      hover_color='#5D6D7E')
        self.clear_btn.pack(side='left', expand=True, fill='x', padx=5)
        
        # Painel de lista de transações
        list_panel = ctk.CTkFrame(self, fg_color='white', corner_radius=10)
        list_panel.grid(row=0, column=1, sticky='nsew', padx=(10, 20), pady=20)
        
        # Cabeçalho da lista
        list_header = ctk.CTkFrame(list_panel, fg_color='transparent')
        list_header.pack(fill='x', padx=20, pady=20)
        
        list_title = ctk.CTkLabel(list_header, text="Transações",
                                 font=('Segoe UI', 18, 'bold'))
        list_title.pack(side='left')
        
        refresh_btn = ctk.CTkButton(list_header, text="🔄", width=40,
                                   command=self.load_transactions)
        refresh_btn.pack(side='right')
        
        # Container scrollable para transações
        self.transactions_list = ctk.CTkScrollableFrame(list_panel, fg_color='transparent')
        self.transactions_list.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def load_categories(self):
        """Carrega categorias disponíveis"""
        try:
            self.categories = self.main_controller.get_all_categories()
            self.category_combo.update_categories(self.categories)
        except Exception as e:
            print(f"Erro ao carregar categorias: {e}")
    
    def load_transactions(self):
        """Carrega lista de transações"""
        # Limpar lista
        for widget in self.transactions_list.winfo_children():
            widget.destroy()
        
        try:
            transactions = self.transaction_controller.get_all_transactions(limit=50)
            
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
                    
                    item = TransactionListItem(
                        self.transactions_list, 
                        trans_data,
                        on_edit=self.edit_transaction,
                        on_delete=self.delete_transaction
                    )
                    item.pack(fill='x', pady=5)
            else:
                no_trans = ctk.CTkLabel(self.transactions_list,
                                       text="Nenhuma transação encontrada",
                                       font=('Segoe UI', 12),
                                       text_color='#7F8C8D')
                no_trans.pack(pady=40)
        except Exception as e:
            print(f"Erro ao carregar transações: {e}")
    
    def save_transaction(self):
        """Salva nova transação ou atualiza existente"""
        try:
            # Coletar dados do formulário
            description = self.description_field.get()
            amount = self.amount_field.widget.get_value()
            category_id = self.category_combo.get_selected_id()
            date = self.date_entry.get_date()
            
            # Converter tipo
            type_map = {'Despesa': 'expense', 'Receita': 'income', 'Transferência': 'transfer'}
            trans_type = type_map[self.type_combo.get()]
            
            # Encontrar enum de método de pagamento
            payment_method_value = self.method_combo.get()
            payment_method = next(
                (pm for pm in PaymentMethod if pm.value == payment_method_value),
                PaymentMethod.CASH
            )
            
            notes = self.notes_entry.get("1.0", "end-1c")
            
            # Validação básica
            if not description or not description.strip():
                ToastNotification(self, "Descrição é obrigatória", type='error')
                return
            
            if amount <= 0:
                ToastNotification(self, "Valor deve ser maior que zero", type='error')
                return
            
            if not category_id:
                ToastNotification(self, "Selecione uma categoria", type='error')
                return
            
            # Preparar dados
            transaction_data = {
                'description': description,
                'amount': amount,
                'category_id': category_id,
                'transaction_date': date,
                'type': trans_type,
                'payment_method': payment_method.name,  # Usar .name para obter o nome do enum
                'notes': notes
            }
            
            if self.editing_id:
                # Atualizar existente
                self.transaction_controller.update_transaction(self.editing_id, **transaction_data)
                ToastNotification(self, "Transação atualizada com sucesso!", type='success')
                self.editing_id = None
            else:
                # Criar nova
                self.transaction_controller.add_transaction(transaction_data)
                ToastNotification(self, "Transação adicionada com sucesso!", type='success')
            
            # Limpar e recarregar
            self.clear_form()
            self.load_transactions()
            
        except ValueError as e:
            ToastNotification(self, str(e), type='error')
        except Exception as e:
            ToastNotification(self, f"Erro ao salvar: {str(e)}", type='error')
            print(f"Erro detalhado: {e}")
    
    def edit_transaction(self, trans_data: dict):
        """Carrega transação para edição"""
        try:
            trans = self.transaction_controller.get_transaction_by_id(trans_data['id'])
            if not trans:
                return
            
            self.editing_id = trans.id
            
            # Preencher formulário
            self.description_field.widget.delete(0, 'end')
            self.description_field.widget.insert(0, trans.description)
            
            self.amount_field.widget.delete(0, 'end')
            from utils import CurrencyFormatter
            self.amount_field.widget.insert(0, CurrencyFormatter.format(trans.amount))
            
            # Selecionar categoria
            for idx, cat in enumerate(self.categories):
                if cat.id == trans.category_id:
                    self.category_combo.set(f"{cat.icon} {cat.name}")
                    break
            
            self.date_entry.set_date(trans.transaction_date)
            
            # Tipo
            type_map = {'expense': 'Despesa', 'income': 'Receita', 'transfer': 'Transferência'}
            trans_type = trans.type if isinstance(trans.type, str) else (trans.type.value if trans.type else 'expense')
            self.type_combo.set(type_map.get(trans_type, 'Despesa'))
            
            # Método de pagamento
            if trans.payment_method:
                payment_val = trans.payment_method if isinstance(trans.payment_method, str) else trans.payment_method.value
                self.method_combo.set(payment_val)
            
            # Notas
            self.notes_entry.delete("1.0", "end")
            if trans.notes:
                self.notes_entry.insert("1.0", trans.notes)
            
            # Atualizar botão
            self.save_btn.configure(text="💾 Atualizar")
            
            ToastNotification(self, "Editando transação", type='info')
            
        except Exception as e:
            print(f"Erro ao editar transação: {e}")
    
    def delete_transaction(self, trans_data: dict):
        """Deleta transação"""
        # Confirmação simples
        if self.transaction_controller.delete_transaction(trans_data['id']):
            ToastNotification(self, "Transação excluída", type='success')
            self.load_transactions()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.editing_id = None
        self.description_field.widget.delete(0, 'end')
        self.amount_field.widget.delete(0, 'end')
        self.date_entry.set_date(datetime.now())
        self.type_combo.set('Despesa')
        self.method_combo.set(PaymentMethod.CASH.value)
        self.notes_entry.delete("1.0", "end")
        self.save_btn.configure(text="💾 Salvar")
        
        if self.categories:
            self.category_combo.set(f"{self.categories[0].icon} {self.categories[0].name}")
    
    def cleanup(self):
        """Limpa recursos"""
        self.transaction_controller.close()
        self.main_controller.close()
