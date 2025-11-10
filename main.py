#!/usr/bin/env python3
"""
Aplicação de Controle Financeiro Pessoal
Desenvolvida com Python, CustomTkinter e SQLAlchemy
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db
from views import MainWindow

def main():
    """Função principal da aplicação"""
    try:
        # Inicializar banco de dados
        print("Inicializando banco de dados...")
        init_db()
        print("Banco de dados inicializado com sucesso!")
        
        # Criar e executar aplicação
        print("Iniciando aplicação...")
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
