@echo off
title Instalador - Controle Financeiro

echo ========================================
echo  Instalador - Controle Financeiro
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Instale Python 3.8 ou superior de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python encontrado!
python --version
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Atualizar pip
echo.
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo  Instalacao concluida!
echo ========================================
echo.
echo Para executar a aplicacao, clique em: run.bat
echo.
pause
