from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Budget(Base):
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(Float, nullable=False)
    month = Column(Integer, nullable=False)  # 1-12
    year = Column(Integer, nullable=False)
    alert_threshold = Column(Float, default=0.8)  # 80% do orçamento
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamento
    category = relationship('Category', back_populates='budgets')
    
    def __repr__(self):
        return f"<Budget(id={self.id}, category_id={self.category_id}, amount={self.amount})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'amount': self.amount,
            'month': self.month,
            'year': self.year,
            'alert_threshold': self.alert_threshold,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
