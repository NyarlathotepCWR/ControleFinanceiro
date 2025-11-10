@echo off
echo ========================================
echo  Criando executavel do Controle Financeiro
echo ========================================
echo.

REM Verificar se pyinstaller esta instalado
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Gerando executavel...
echo.

REM Criar executavel
pyinstaller --name="ControleFinanceiro" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --add-data "models;models" ^
    --add-data "views;views" ^
    --add-data "controllers;controllers" ^
    --add-data "utils;utils" ^
    --hidden-import=sqlalchemy ^
    --hidden-import=customtkinter ^
    --hidden-import=matplotlib ^
    --hidden-import=pydantic ^
    --hidden-import=PIL ^
    --hidden-import=tkcalendar ^
    --collect-all customtkinter ^
    main.py

echo.
echo ========================================
echo  Executavel criado em: dist\ControleFinanceiro.exe
echo ========================================
echo.
pause
