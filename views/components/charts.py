import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import List, Dict, Any
import matplotlib
matplotlib.use('Agg')

class ChartGenerator:
    """Gerador de gráficos para relatórios"""
    
    @staticmethod
    def create_pie_chart(data: List[Dict[str, Any]], title: str = "Distribuição por Categoria") -> Figure:
        """Cria gráfico de pizza para categorias"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        if not data:
            ax.text(0.5, 0.5, 'Sem dados disponíveis', ha='center', va='center')
            return fig
        
        labels = [item['name'] for item in data]
        sizes = [item['total'] for item in data]
        colors = [item.get('color', '#2E86AB') for item in data]
        
        # Criar gráfico
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90
        )
        
        # Estilização
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_line_chart(data: List[Dict[str, Any]], title: str = "Evolução Mensal") -> Figure:
        """Cria gráfico de linha para evolução temporal"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if not data:
            ax.text(0.5, 0.5, 'Sem dados disponíveis', ha='center', va='center')
            return fig
        
        months = [item['month_name'] for item in data]
        income = [item['income'] for item in data]
        expenses = [item['expenses'] for item in data]
        
        # Plotar linhas
        ax.plot(months, income, marker='o', linewidth=2, label='Entradas', color='#27AE60')
        ax.plot(months, expenses, marker='s', linewidth=2, label='Saídas', color='#E74C3C')
        
        # Estilização
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Mês', fontsize=11)
        ax.set_ylabel('Valor (R$)', fontsize=11)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Formatar eixo Y como moeda
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def create_bar_chart(data: List[Dict[str, Any]], title: str = "Comparativo") -> Figure:
        """Cria gráfico de barras"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if not data:
            ax.text(0.5, 0.5, 'Sem dados disponíveis', ha='center', va='center')
            return fig
        
        categories = [item['name'] for item in data]
        values = [item['total'] for item in data]
        colors = [item.get('color', '#2E86AB') for item in data]
        
        bars = ax.bar(categories, values, color=colors)
        
        # Adicionar valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'R$ {height:,.2f}',
                   ha='center', va='bottom', fontsize=9)
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel('Valor (R$)', fontsize=11)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x:,.0f}'))
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    @staticmethod
    def embed_chart(parent, figure: Figure):
        """Incorpora gráfico em widget Tkinter"""
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        return canvas.get_tk_widget()
