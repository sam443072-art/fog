#!/bin/bash
# deploy.sh
# Script de despliegue automatizado para Google Cloud Run

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ARK Tribe Manager - Cloud Run Deploy${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Configuración
PROJECT_ID="fog-astra"
SERVICE_NAME="ark-tribe-manager"
REGION="us-central1"
MEMORY="512Mi"
PORT="8080"

# Verificar que gcloud esté instalado
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI no está instalado${NC}"
    echo "Instala desde: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configurar proyecto
echo -e "${BLUE}Configurando proyecto...${NC}"
gcloud config set project $PROJECT_ID

# Habilitar APIs necesarias
echo -e "\n${BLUE}Habilitando APIs necesarias...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Desplegar en Cloud Run
echo -e "\n${BLUE}Desplegando en Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port $PORT \
  --memory $MEMORY \
  --min-instances 0 \
  --max-instances 10 \
  --timeout 300 \
  --cpu 1

# Verificar despliegue
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ Despliegue exitoso!${NC}"
    echo -e "${GREEN}========================================${NC}\n"
    
    # Obtener URL del servicio
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
    echo -e "${GREEN}URL de la aplicación:${NC}"
    echo -e "${BLUE}$SERVICE_URL${NC}\n"
else
    echo -e "\n${RED}========================================${NC}"
    echo -e "${RED}  ✗ Error en el despliegue${NC}"
    echo -e "${RED}========================================${NC}\n"
    exit 1
fi
