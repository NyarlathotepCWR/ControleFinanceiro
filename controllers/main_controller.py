from models import get_session, Category
from typing import List, Optional

class MainController:
    """Controlador principal da aplicação"""
    
    def __init__(self):
        self.session = get_session()
    
    def get_all_categories(self, active_only: bool = True) -> List[Category]:
        """Retorna todas as categorias"""
        query = self.session.query(Category)
        if active_only:
            query = query.filter(Category.is_active == True)
        return query.order_by(Category.name).all()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Retorna uma categoria por ID"""
        return self.session.query(Category).filter(Category.id == category_id).first()
    
    def add_category(self, name: str, icon: str = '📁', color: str = '#2E86AB') -> Category:
        """Adiciona uma nova categoria"""
        category = Category(name=name, icon=icon, color=color)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category
    
    def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        """Atualiza uma categoria"""
        category = self.get_category_by_id(category_id)
        if category:
            for key, value in kwargs.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            self.session.commit()
            self.session.refresh(category)
        return category
    
    def delete_category(self, category_id: int) -> bool:
        """Desativa uma categoria (soft delete)"""
        category = self.get_category_by_id(category_id)
        if category:
            category.is_active = False
            self.session.commit()
            return True
        return False
    
    def close(self):
        """Fecha a sessão do banco de dados"""
        self.session.close()
