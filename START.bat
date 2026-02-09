# START.bat
# Script de inicio rápido para Windows

@echo off
cls
echo ========================================
echo   ARK TRIBE MANAGER
echo   FOG Tribe
echo ========================================
echo.
echo Selecciona una opcion:
echo.
echo 1. Ejecutar en modo Ventana (Escritorio)
echo 2. Ejecutar en modo Web (Navegador)
echo 3. Instalar dependencias
echo 4. Salir
echo.
set /p choice="Opcion (1-4): "

if "%choice%"=="1" goto desktop
if "%choice%"=="2" goto web
if "%choice%"=="3" goto install
if "%choice%"=="4" goto end

:desktop
echo.
echo Iniciando en modo Ventana...
python run_local.py
goto end

:web
echo.
echo Iniciando en modo Web...
echo Abre tu navegador en: http://localhost:8080
python run_web.py
goto end

:install
echo.
echo Instalando dependencias...
pip install -r requirements.txt
echo.
echo Instalacion completada!
pause
goto end

:end
