from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    icon = Column(String(10), default='📁')
    color = Column(String(7), default='#2E86AB')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamento com transações
    transactions = relationship('Transaction', back_populates='category', cascade='all, delete-orphan')
    budgets = relationship('Budget', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'color': self.color,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
