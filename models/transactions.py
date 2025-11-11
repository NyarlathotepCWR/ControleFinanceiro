from sqlalchemy import Column, Integer, Float, String, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class TransactionType(enum.Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'

class PaymentMethod(enum.Enum):
    CASH = 'Dinheiro'
    DEBIT_CARD = 'Cartão de Débito'
    CREDIT_CARD = 'Cartão de Crédito'
    PIX = 'PIX'
    BANK_TRANSFER = 'Transferência Bancária'
    OTHER = 'Outro'

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    description = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    transaction_date = Column(DateTime, nullable=False, default=datetime.now)
    type = Column(String(20), nullable=False, default='expense')
    payment_method = Column(String(50), default='Dinheiro')
    tags = Column(JSON, default=list)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamento
    category = relationship('Category', back_populates='transactions')
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, description='{self.description}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'type': self.type,
            'payment_method': self.payment_method,
            'tags': self.tags or [],
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
