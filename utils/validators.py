from datetime import datetime
from typing import Any

class FinancialValidators:
    """Validadores para dados financeiros"""
    
    @staticmethod
    def validate_amount(amount: Any) -> float:
        """Valida e converte valor monetário"""
        try:
            value = float(amount)
            if value <= 0:
                raise ValueError("Valor deve ser positivo")
            return round(value, 2)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Valor inválido: {amount}") from e
    
    @staticmethod
    def validate_date(date_input: Any) -> datetime:
        """Valida e converte data"""
        if isinstance(date_input, datetime):
            return date_input
        
        if isinstance(date_input, str):
            formats = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]
            for fmt in formats:
                try:
                    return datetime.strptime(date_input, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Data inválida: {date_input}. Use DD/MM/AAAA")
        
        raise ValueError("Tipo de data inválido")
    
    @staticmethod
    def validate_description(description: str, max_length: int = 200) -> str:
        """Valida descrição"""
        if not description or not description.strip():
            raise ValueError("Descrição não pode estar vazia")
        
        desc = description.strip()
        if len(desc) > max_length:
            raise ValueError(f"Descrição muito longa (máximo {max_length} caracteres)")
        
        return desc
    
    @staticmethod
    def validate_category_id(category_id: Any) -> int:
        """Valida ID de categoria"""
        try:
            cat_id = int(category_id)
            if cat_id <= 0:
                raise ValueError("ID de categoria inválido")
            return cat_id
        except (TypeError, ValueError) as e:
            raise ValueError(f"ID de categoria inválido: {category_id}") from e
