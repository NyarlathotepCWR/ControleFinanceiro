from models import get_session, Transaction, TransactionType, PaymentMethod
from utils import FinancialValidators
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy import extract, func, and_

class TransactionController:
    """Controlador de transações"""
    
    def __init__(self):
        self.session = get_session()
    
    def add_transaction(self, transaction_data: Dict[str, Any]) -> Transaction:
        """Adiciona uma nova transação com validação"""
        # Validações
        amount = FinancialValidators.validate_amount(transaction_data['amount'])
        description = FinancialValidators.validate_description(transaction_data['description'])
        category_id = FinancialValidators.validate_category_id(transaction_data['category_id'])
        transaction_date = FinancialValidators.validate_date(transaction_data.get('transaction_date', datetime.now()))
        
        # Conversão de enums
        trans_type = transaction_data.get('type', 'expense')
        if not isinstance(trans_type, str):
            trans_type = trans_type.value if hasattr(trans_type, 'value') else 'expense'
        
        payment_method = transaction_data.get('payment_method', 'Dinheiro')
        if not isinstance(payment_method, str):
            payment_method = payment_method.value if hasattr(payment_method, 'value') else 'Dinheiro'
        else:
            # Converter nome do enum para valor se necessário
            try:
                pm_enum = PaymentMethod[payment_method]
                payment_method = pm_enum.value
            except (KeyError, AttributeError):
                # Já é um valor ou inválido, manter como está ou usar padrão
                if payment_method not in [pm.value for pm in PaymentMethod]:
                    payment_method = 'Dinheiro'
        
        # Criação da transação
        transaction = Transaction(
            amount=amount,
            description=description,
            category_id=category_id,
            transaction_date=transaction_date,
            type=trans_type,
            payment_method=payment_method,
            tags=transaction_data.get('tags', []),
            notes=transaction_data.get('notes', '')
        )
        
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction
    
    def get_all_transactions(self, limit: Optional[int] = None) -> List[Transaction]:
        """Retorna todas as transações"""
        query = self.session.query(Transaction).order_by(Transaction.transaction_date.desc())
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def get_transactions_by_period(self, month: int, year: int) -> List[Transaction]:
        """Retorna transações de um período específico"""
        return self.session.query(Transaction).filter(
            extract('month', Transaction.transaction_date) == month,
            extract('year', Transaction.transaction_date) == year
        ).order_by(Transaction.transaction_date.desc()).all()
    
    def get_transactions_by_category(self, category_id: int, month: Optional[int] = None, year: Optional[int] = None) -> List[Transaction]:
        """Retorna transações de uma categoria"""
        query = self.session.query(Transaction).filter(Transaction.category_id == category_id)
        
        if month and year:
            query = query.filter(
                extract('month', Transaction.transaction_date) == month,
                extract('year', Transaction.transaction_date) == year
            )
        
        return query.order_by(Transaction.transaction_date.desc()).all()
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Retorna uma transação por ID"""
        return self.session.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    def update_transaction(self, transaction_id: int, **kwargs) -> Optional[Transaction]:
        """Atualiza uma transação"""
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            # Validar campos se presentes
            if 'amount' in kwargs:
                kwargs['amount'] = FinancialValidators.validate_amount(kwargs['amount'])
            if 'description' in kwargs:
                kwargs['description'] = FinancialValidators.validate_description(kwargs['description'])
            if 'transaction_date' in kwargs:
                kwargs['transaction_date'] = FinancialValidators.validate_date(kwargs['transaction_date'])
            
            for key, value in kwargs.items():
                if hasattr(transaction, key):
                    setattr(transaction, key, value)
            
            self.session.commit()
            self.session.refresh(transaction)
        return transaction
    
    def delete_transaction(self, transaction_id: int) -> bool:
        """Deleta uma transação"""
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            self.session.delete(transaction)
            self.session.commit()
            return True
        return False
    
    def get_monthly_summary(self, month: int, year: int) -> Dict[str, float]:
        """Retorna resumo mensal (total de entradas, saídas e saldo)"""
        transactions = self.get_transactions_by_period(month, year)
        
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expenses
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'count': len(transactions)
        }
    
    def get_expenses_by_category(self, month: int, year: int) -> List[Dict[str, Any]]:
        """Retorna gastos por categoria no período"""
        result = self.session.query(
            Transaction.category_id,
            func.sum(Transaction.amount).label('total')
        ).filter(
            and_(
                extract('month', Transaction.transaction_date) == month,
                extract('year', Transaction.transaction_date) == year,
                Transaction.type == 'expense'
            )
        ).group_by(Transaction.category_id).all()
        
        return [{'category_id': r.category_id, 'total': r.total} for r in result]
    
    def close(self):
        """Fecha a sessão do banco de dados"""
        self.session.close()
