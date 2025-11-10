import customtkinter as ctk
from datetime import datetime
from typing import Callable, Optional, List
from tkcalendar import Calendar
from utils import CurrencyFormatter

class CurrencyEntry(ctk.CTkEntry):
    """Campo de entrada para valores monetários"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self._format_currency)
        self.bind('<FocusOut>', self._validate)
    
    def _format_currency(self, event=None):
        """Formata o valor durante a digitação"""
        pass  # Implementação básica, pode ser melhorada
    
    def _validate(self, event=None):
        """Valida o valor ao perder o foco"""
        try:
            value = self.get()
            if value and value.strip():
                parsed = CurrencyFormatter.parse(value)
                formatted = CurrencyFormatter.format(parsed)
                self.delete(0, 'end')
                self.insert(0, formatted)
        except ValueError:
            pass
    
    def get_value(self) -> float:
        """Retorna o valor numérico"""
        try:
            return CurrencyFormatter.parse(self.get())
        except:
            return 0.0

class DatePickerEntry(ctk.CTkEntry):
    """Campo de entrada de data com seletor"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_date = datetime.now()
        self.configure(state='readonly')
        self.bind('<Button-1>', self._show_calendar)
        self._set_display()
    
    def _show_calendar(self, event=None):
        """Exibe seletor de data"""
        top = ctk.CTkToplevel(self)
        top.title("Selecionar Data")
        top.geometry("300x300")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy',
                      year=self.selected_date.year,
                      month=self.selected_date.month,
                      day=self.selected_date.day)
        cal.pack(pady=20, padx=20)
        
        def select():
            date_str = cal.get_date()
            self.selected_date = datetime.strptime(date_str, '%d/%m/%Y')
            self._set_display()
            top.destroy()
        
        btn = ctk.CTkButton(top, text="Confirmar", command=select)
        btn.pack(pady=10)
    
    def _set_display(self):
        """Atualiza display da data"""
        self.configure(state='normal')
        self.delete(0, 'end')
        self.insert(0, self.selected_date.strftime('%d/%m/%Y'))
        self.configure(state='readonly')
    
    def get_date(self) -> datetime:
        """Retorna a data selecionada"""
        return self.selected_date
    
    def set_date(self, date: datetime):
        """Define a data"""
        self.selected_date = date
        self._set_display()

class CategoryComboBox(ctk.CTkComboBox):
    """ComboBox customizado para categorias"""
    
    def __init__(self, master, categories: List = None, **kwargs):
        self.categories = categories or []
        values = [f"{cat.icon} {cat.name}" if hasattr(cat, 'icon') else cat.name 
                 for cat in self.categories]
        
        super().__init__(master, values=values or ["Nenhuma categoria"], **kwargs)
        
        if values:
            self.set(values[0])
    
    def update_categories(self, categories: List):
        """Atualiza lista de categorias"""
        self.categories = categories
        values = [f"{cat.icon} {cat.name}" if hasattr(cat, 'icon') else cat.name 
                 for cat in categories]
        self.configure(values=values or ["Nenhuma categoria"])
        if values:
            self.set(values[0])
    
    def get_selected_id(self) -> Optional[int]:
        """Retorna ID da categoria selecionada"""
        try:
            index = self.cget('values').index(self.get())
            return self.categories[index].id
        except:
            return None

class FormField(ctk.CTkFrame):
    """Campo de formulário com label"""
    
    def __init__(self, master, label_text: str, widget_class, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        self.label = ctk.CTkLabel(self, text=label_text, anchor='w')
        self.label.pack(fill='x', pady=(0, 5))
        
        self.widget = widget_class(self, **kwargs)
        self.widget.pack(fill='x')
    
    def get(self):
        """Retorna valor do widget"""
        return self.widget.get()
    
    def set(self, value):
        """Define valor do widget"""
        if hasattr(self.widget, 'set'):
            self.widget.set(value)
        else:
            self.widget.delete(0, 'end')
            self.widget.insert(0, value)

class ToastNotification(ctk.CTkToplevel):
    """Notificação toast"""
    
    def __init__(self, master, message: str, duration: int = 2000, type: str = "info"):
        super().__init__(master)
        
        # Configurações da janela
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        # Cores por tipo
        colors = {
            'info': '#2E86AB',
            'success': '#27AE60',
            'warning': '#F39C12',
            'error': '#E74C3C'
        }
        
        # Frame principal
        frame = ctk.CTkFrame(self, fg_color=colors.get(type, colors['info']))
        frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Mensagem
        label = ctk.CTkLabel(frame, text=message, text_color='white', 
                            font=('Segoe UI', 12, 'bold'))
        label.pack(padx=20, pady=15)
        
        # Posicionar no centro superior da tela
        self.update_idletasks()
        width = self.winfo_width()
        screen_width = master.winfo_screenwidth()
        x = (screen_width - width) // 2
        self.geometry(f'+{x}+50')
        
        # Auto-fechar
        self.after(duration, self.destroy)
