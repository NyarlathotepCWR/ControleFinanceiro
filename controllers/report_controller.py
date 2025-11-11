from models import get_session, Transaction, TransactionType, Category
from datetime import datetime
from typing import Dict, List, Any
from sqlalchemy import extract, func
import calendar

class ReportController:
    """Controlador de relatórios e análises"""
    
    def __init__(self):
        self.session = get_session()
    
    def get_dashboard_metrics(self, month: int, year: int) -> Dict[str, Any]:
        """Retorna métricas do dashboard para o período"""
        transactions = self.session.query(Transaction).filter(
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year
        ).all()
        
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expenses
        
        # Comparação com mês anterior
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        
        prev_transactions = self.session.query(Transaction).filter(
            extract('month', Transaction.transaction_date) == prev_month,
            extract('year', Transaction.transaction_date) == prev_year
        ).all()
        
        prev_expenses = sum(t.amount for t in prev_transactions if t.type == 'expense')
        expense_variation = ((expenses - prev_expenses) / prev_expenses * 100) if prev_expenses > 0 else 0
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'transaction_count': len(transactions),
            'expense_variation': expense_variation,
            'avg_transaction': expenses / len([t for t in transactions if t.type == 'expense']) if expenses > 0 else 0
        }
    
    def get_category_breakdown(self, month: int, year: int) -> List[Dict[str, Any]]:
        """Retorna distribuição de gastos por categoria"""
        result = self.session.query(
            Category.name,
            Category.color,
            Category.icon,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).join(Transaction).filter(
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year,
            Transaction.type == 'expense'
        ).group_by(Category.id).all()
        
        total_expenses = sum(r.total for r in result)
        
        return [{
            'name': r.name,
            'color': r.color,
            'icon': r.icon,
            'total': r.total,
            'count': r.count,
            'percentage': (r.total / total_expenses * 100) if total_expenses > 0 else 0
        } for r in result]
    
    def get_monthly_evolution(self, year: int, months: int = 6) -> List[Dict[str, Any]]:
        """Retorna evolução mensal dos últimos N meses"""
        evolution = []
        current_date = datetime.now()
        
        for i in range(months - 1, -1, -1):
            target_month = current_date.month - i
            target_year = current_date.year
            
            if target_month <= 0:
                target_month += 12
                target_year -= 1
            
            transactions = self.session.query(Transaction).filter(
                extract('month', Transaction.transaction_date) == target_month,
                extract('year', Transaction.transaction_date) == target_year
            ).all()
            
            income = sum(t.amount for t in transactions if t.type == 'income')
            expenses = sum(t.amount for t in transactions if t.type == 'expense')
            
            evolution.append({
                'month': target_month,
                'year': target_year,
                'month_name': calendar.month_abbr[target_month],
                'income': income,
                'expenses': expenses,
                'balance': income - expenses
            })
        
        return evolution
    
    def get_top_expenses(self, month: int, year: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Retorna as maiores despesas do período"""
        transactions = self.session.query(Transaction).filter(
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year,
            Transaction.type == 'expense'
        ).order_by(Transaction.amount.desc()).limit(limit).all()
        
        return [t.to_dict() for t in transactions]
    
    def get_payment_method_breakdown(self, month: int, year: int) -> List[Dict[str, Any]]:
        """Retorna distribuição por método de pagamento"""
        result = self.session.query(
            Transaction.payment_method,
            func.sum(Transaction.amount).label('total'),
            func.count(Transaction.id).label('count')
        ).filter(
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year,
            Transaction.type == 'expense'
        ).group_by(Transaction.payment_method).all()
        
        return [{
            'method': r.payment_method if r.payment_method else 'Desconhecido',
            'total': r.total,
            'count': r.count
        } for r in result]
    
    def close(self):
        """Fecha a sessão do banco de dados"""
        self.session.close()
