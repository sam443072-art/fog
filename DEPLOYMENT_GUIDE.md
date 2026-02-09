# DEPLOYMENT_GUIDE.md

# Guía de Despliegue en Google Cloud Run

## 📋 Requisitos Previos

1. **Cuenta de Google Cloud**
   - Crear cuenta en [Google Cloud Console](https://console.cloud.google.com)
   - Habilitar facturación (Cloud Run tiene capa gratuita)

2. **Google Cloud SDK**
   - Descargar e instalar desde [aquí](https://cloud.google.com/sdk/docs/install)
   - Verificar instalación: `gcloud --version`

3. **Proyecto de Google Cloud**
   - Usar el proyecto existente: `fog-astra`
   - O crear uno nuevo en la consola

## 🚀 Métodos de Despliegue

### Método 1: Script Automatizado (Recomendado)

**Windows:**

```bash
deploy.bat
```

**Linux/Mac:**

```bash
chmod +x deploy.sh
./deploy.sh
```

### Método 2: Comando Manual

```bash
# 1. Autenticarse
gcloud auth login

# 2. Configurar proyecto
gcloud config set project fog-astra

# 3. Habilitar APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# 4. Desplegar
gcloud run deploy ark-tribe-manager \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi
```

### Método 3: Cloud Build (CI/CD)

1. Conectar repositorio Git a Cloud Build
2. Configurar trigger automático
3. Usar `cloudbuild.yaml` incluido

## 🔧 Configuración Post-Despliegue

### 1. Configurar Dominio Personalizado (Opcional)

```bash
gcloud run services update ark-tribe-manager \
  --region us-central1 \
  --add-cloudsql-instances fog-astra:us-central1:ark-db
```

### 2. Configurar Variables de Entorno (Si usas .env)

```bash
gcloud run services update ark-tribe-manager \
  --region us-central1 \
  --set-env-vars "FIREBASE_API_KEY=tu_api_key"
```

### 3. Configurar Autenticación (Si quieres restringir acceso)

```bash
gcloud run services update ark-tribe-manager \
  --region us-central1 \
  --no-allow-unauthenticated
```

## 📊 Monitoreo y Logs

### Ver Logs en Tiempo Real

```bash
gcloud run services logs tail ark-tribe-manager --region us-central1
```

### Ver Métricas

1. Ir a [Cloud Console](https://console.cloud.google.com)
2. Navegar a Cloud Run > ark-tribe-manager
3. Ver pestaña "Metrics"

## 💰 Costos Estimados

**Capa Gratuita de Cloud Run:**

- 2 millones de requests/mes
- 360,000 GB-segundos de memoria
- 180,000 vCPU-segundos

**Estimación para esta app:**

- Con 512Mi de memoria y tráfico moderado: **$0-5/mes**

## 🔒 Seguridad

### Reglas de Firebase

Asegúrate de tener estas reglas en Firebase Realtime Database:

```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null",
    "generators": {
      ".indexOn": ["created_by", "start_timestamp"]
    },
    "tasks": {
      ".indexOn": ["tag", "timestamp"]
    },
    "members": {
      ".indexOn": ["trust", "roles"]
    },
    "admin_status": {
      ".indexOn": ["active", "last_heartbeat"]
    }
  }
}
```

### CORS (Si es necesario)

Si tienes problemas de CORS, añade esto al `main.py`:

```python
from flet import Page

def main(page: Page):
    page.web_security = False  # Solo para desarrollo
    # ... resto del código
```

## 🔄 Actualizar Aplicación

Para actualizar la aplicación desplegada:

1. Hacer cambios en el código
2. Ejecutar nuevamente el script de despliegue:
   ```bash
   deploy.bat  # Windows
   ./deploy.sh # Linux/Mac
   ```

## 🐛 Troubleshooting

### Error: "Permission denied"

```bash
gcloud auth login
gcloud auth application-default login
```

### Error: "Quota exceeded"

- Verificar límites en Cloud Console
- Aumentar cuota si es necesario

### Error: "Port already in use"

- Cambiar puerto en `run_web.py` o `Dockerfile`

### La app no carga

1. Verificar logs: `gcloud run services logs tail ark-tribe-manager`
2. Verificar que Firebase esté configurado correctamente
3. Verificar que las APIs estén habilitadas

## 📞 Soporte

Para problemas con:

- **Google Cloud**: [Documentación oficial](https://cloud.google.com/run/docs)
- **Flet**: [Documentación de Flet](https://flet.dev/docs)
- **Firebase**: [Documentación de Firebase](https://firebase.google.com/docs)

## 🎯 Próximos Pasos

1. Configurar dominio personalizado
2. Implementar SSL/HTTPS (automático en Cloud Run)
3. Configurar backups de Firebase
4. Implementar monitoreo con Cloud Monitoring
5. Configurar alertas de error

---

**¡Listo!** Tu aplicación ARK Tribe Manager está en la nube 🚀
