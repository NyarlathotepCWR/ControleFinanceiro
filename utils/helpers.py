from datetime import datetime
from typing import Tuple

class ColorScheme:
    """Esquema de cores da aplicação"""
    PRIMARY = "#2E86AB"
    SECONDARY = "#A23B72"
    SUCCESS = "#27AE60"
    WARNING = "#F39C12"
    DANGER = "#E74C3C"
    LIGHT = "#ECF0F1"
    DARK = "#2C3E50"
    BACKGROUND = "#F8F9FA"
    WHITE = "#FFFFFF"
    GRAY = "#7F8C8D"
    LIGHT_GRAY = "#BDC3C7"

def get_month_name(month: int) -> str:
    """Retorna o nome do mês em português"""
    months = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    if 1 <= month <= 12:
        return months[month - 1]
    return ""

def get_current_month_year() -> Tuple[int, int]:
    """Retorna o mês e ano atuais"""
    now = datetime.now()
    return now.month, now.year

def get_previous_month_year(month: int, year: int) -> Tuple[int, int]:
    """Retorna o mês e ano anteriores"""
    if month == 1:
        return 12, year - 1
    return month - 1, year
