# deploy.bat
# Script de despliegue para Windows

@echo off
echo ========================================
echo   ARK Tribe Manager - Cloud Run Deploy
echo ========================================
echo.

REM Configuración
set PROJECT_ID=fog-astra
set SERVICE_NAME=ark-tribe-manager
set REGION=us-central1
set MEMORY=512Mi
set PORT=8080

REM Verificar que gcloud esté instalado
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: gcloud CLI no esta instalado
    echo Instala desde: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

REM Configurar proyecto
echo Configurando proyecto...
call gcloud config set project %PROJECT_ID%

REM Habilitar APIs necesarias
echo.
echo Habilitando APIs necesarias...
call gcloud services enable cloudbuild.googleapis.com
call gcloud services enable run.googleapis.com

REM Desplegar en Cloud Run
echo.
echo Desplegando en Cloud Run...
call gcloud run deploy %SERVICE_NAME% ^
  --source . ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --port %PORT% ^
  --memory %MEMORY% ^
  --min-instances 0 ^
  --max-instances 10 ^
  --timeout 300 ^
  --cpu 1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Despliegue exitoso!
    echo ========================================
    echo.
    
    REM Obtener URL del servicio
    for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"') do set SERVICE_URL=%%i
    echo URL de la aplicacion:
    echo %SERVICE_URL%
    echo.
) else (
    echo.
    echo ========================================
    echo   Error en el despliegue
    echo ========================================
    echo.
    exit /b 1
)

pause
