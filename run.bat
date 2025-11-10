@echo off
title Controle Financeiro

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Executar aplicacao
python main.py

REM Pausar se houver erro
if %errorlevel% neq 0 (
    echo.
    echo Erro ao executar a aplicacao!
    pause
)
