#!/bin/bash

echo "========================================"
echo " Instalador - Controle Financeiro"
echo "========================================"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 nao encontrado. Instale Python 3.8 ou superior."
    exit 1
fi

echo "Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Instalar dependencias
echo ""
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo " Instalacao concluida!"
echo "========================================"
echo ""
echo "Para executar a aplicacao:"
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    echo "  - Windows: Clique duas vezes em run.bat"
else
    echo "  - Linux/Mac: Execute ./run.sh"
fi
echo ""
