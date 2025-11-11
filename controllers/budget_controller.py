from models import get_session, Budget, Transaction, TransactionType
from typing import List, Optional, Dict, Any
from sqlalchemy import extract, func

class BudgetController:
    """Controlador de orçamentos"""
    
    def __init__(self):
        self.session = get_session()
    
    def add_budget(self, category_id: int, amount: float, month: int, year: int, alert_threshold: float = 0.8) -> Budget:
        """Adiciona um novo orçamento"""
        # Verificar se já existe orçamento para essa categoria/período
        existing = self.get_budget(category_id, month, year)
        if existing:
            # Atualizar existente
            existing.amount = amount
            existing.alert_threshold = alert_threshold
            existing.is_active = True
            self.session.commit()
            self.session.refresh(existing)
            return existing
        
        budget = Budget(
            category_id=category_id,
            amount=amount,
            month=month,
            year=year,
            alert_threshold=alert_threshold
        )
        
        self.session.add(budget)
        self.session.commit()
        self.session.refresh(budget)
        return budget
    
    def get_budget(self, category_id: int, month: int, year: int) -> Optional[Budget]:
        """Retorna orçamento para categoria/período"""
        return self.session.query(Budget).filter(
            Budget.category_id == category_id,
            Budget.month == month,
            Budget.year == year,
            Budget.is_active == True
        ).first()
    
    def get_all_budgets(self, month: int, year: int) -> List[Budget]:
        """Retorna todos os orçamentos ativos de um período"""
        return self.session.query(Budget).filter(
            Budget.month == month,
            Budget.year == year,
            Budget.is_active == True
        ).all()
    
    def get_budget_status(self, category_id: int, month: int, year: int) -> Dict[str, Any]:
        """Retorna status do orçamento (gasto vs planejado)"""
        budget = self.get_budget(category_id, month, year)
        
        if not budget:
            return {
                'has_budget': False,
                'budgeted': 0,
                'spent': 0,
                'remaining': 0,
                'percentage': 0,
                'alert': False
            }
        
        # Calcular gasto real
        spent = self.session.query(func.sum(Transaction.amount)).filter(
            Transaction.category_id == category_id,
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year,
            Transaction.type == 'expense'
        ).scalar() or 0
        
        remaining = budget.amount - spent
        percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
        alert = percentage >= (budget.alert_threshold * 100)
        
        return {
            'has_budget': True,
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'alert': alert,
            'threshold': budget.alert_threshold * 100
        }
    
    def get_all_budget_status(self, month: int, year: int) -> List[Dict[str, Any]]:
        """Retorna status de todos os orçamentos do período"""
        budgets = self.get_all_budgets(month, year)
        
        result = []
        for budget in budgets:
            status = self.get_budget_status(budget.category_id, month, year)
            status['category_id'] = budget.category_id
            status['category_name'] = budget.category.name if budget.category else 'Desconhecida'
            status['category_icon'] = budget.category.icon if budget.category else '📁'
            status['category_color'] = budget.category.color if budget.category else '#2E86AB'
            result.append(status)
        
        return result
    
    def update_budget(self, budget_id: int, **kwargs) -> Optional[Budget]:
        """Atualiza um orçamento"""
        budget = self.session.query(Budget).filter(Budget.id == budget_id).first()
        if budget:
            for key, value in kwargs.items():
                if hasattr(budget, key):
                    setattr(budget, key, value)
            self.session.commit()
            self.session.refresh(budget)
        return budget
    
    def delete_budget(self, budget_id: int) -> bool:
        """Desativa um orçamento"""
        budget = self.session.query(Budget).filter(Budget.id == budget_id).first()
        if budget:
            budget.is_active = False
            self.session.commit()
            return True
        return False
    
    def close(self):
        """Fecha a sessão do banco de dados"""
        self.session.close()
