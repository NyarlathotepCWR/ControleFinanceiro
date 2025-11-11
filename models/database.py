from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys

Base = declarative_base()

# Detectar se está rodando como executável PyInstaller
if getattr(sys, 'frozen', False):
    # Executável: salvar DB no mesmo diretório do .exe
    application_path = os.path.dirname(sys.executable)
else:
    # Script Python: salvar DB no diretório do script
    application_path = os.path.dirname(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(application_path, 'financial_data.db')
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    """Retorna uma nova sessão de banco de dados"""
    return SessionLocal()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    from .categories import Category
    from .transactions import Transaction
    from .budgets import Budget
    
    Base.metadata.create_all(bind=engine)
    
    # Inserir categorias padrão se o banco estiver vazio
    session = get_session()
    if session.query(Category).count() == 0:
        default_categories = [
            Category(name='Alimentação', icon='🍽️', color='#E74C3C'),
            Category(name='Transporte', icon='🚗', color='#3498DB'),
            Category(name='Moradia', icon='🏠', color='#9B59B6'),
            Category(name='Saúde', icon='⚕️', color='#1ABC9C'),
            Category(name='Educação', icon='📚', color='#F39C12'),
            Category(name='Lazer', icon='🎮', color='#E67E22'),
            Category(name='Vestuário', icon='👔', color='#95A5A6'),
            Category(name='Salário', icon='💰', color='#27AE60'),
            Category(name='Outros', icon='📦', color='#34495E'),
        ]
        session.add_all(default_categories)
        session.commit()
    session.close()
