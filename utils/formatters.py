from datetime import datetime
from typing import Union

class CurrencyFormatter:
    """Formatadores para valores monetários"""
    
    @staticmethod
    def format(value: float) -> str:
        """Formata valor para moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
    
    @staticmethod
    def parse(value: str) -> float:
        """Converte string de moeda para float"""
        # Remove R$, espaços e pontos de milhar
        cleaned = value.replace('R$', '').replace(' ', '').replace('.', '')
        # Substitui vírgula decimal por ponto
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            raise ValueError(f"Valor inválido: {value}")

class DateFormatter:
    """Formatadores para datas"""
    
    @staticmethod
    def format(date: datetime, format_str: str = "%d/%m/%Y") -> str:
        """Formata datetime para string"""
        if not isinstance(date, datetime):
            return ""
        return date.strftime(format_str)
    
    @staticmethod
    def format_month_year(date: datetime) -> str:
        """Formata para mês/ano (ex: Janeiro/2024)"""
        months = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        return f"{months[date.month - 1]}/{date.year}"
    
    @staticmethod
    def parse(date_str: str, format_str: str = "%d/%m/%Y") -> datetime:
        """Converte string para datetime"""
        return datetime.strptime(date_str, format_str)
