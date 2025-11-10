#!/bin/bash

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Executar aplicacao
python3 main.py

# Verificar erro
if [ $? -ne 0 ]; then
    echo ""
    echo "Erro ao executar a aplicacao!"
    read -p "Pressione Enter para continuar..."
fi
