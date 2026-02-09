# ARK Tribe Manager Web

Aplicación web premium para gestión de tribu de ARK: Survival Ascended, construida con Flet y Firebase.

## 🎯 Características

- **Autenticación Firebase**: Login seguro con email/password
- **Server Status**: Monitoreo en tiempo real del servidor ARK
- **Generadores**: Sistema de countdown para combustible de generadores
- **Tareas**: Gestión de tareas con tags de roles (ADMIN, Builder, GH, BR)
- **Miembros**: Administración de miembros con niveles de confianza y multi-roles
- **Heartbeat System**: Visualización de admins activos en tiempo real

## 🚀 Instalación Local

### Requisitos

- Python 3.11+
- pip

### Pasos

1. Clonar o descargar el proyecto

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:

```bash
python main.py
```

La aplicación se abrirá en una ventana de escritorio.

## 🌐 Despliegue en Google Cloud Run

### Requisitos

- Google Cloud SDK instalado
- Proyecto de Google Cloud configurado
- Docker instalado (opcional, Cloud Build lo hace automáticamente)

### Pasos

1. Autenticarse en Google Cloud:

```bash
gcloud auth login
gcloud config set project [TU-PROJECT-ID]
```

2. Habilitar APIs necesarias:

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

3. Desplegar en Cloud Run:

```bash
gcloud run deploy ark-tribe-manager \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi
```

4. La URL de la aplicación se mostrará al finalizar el despliegue.

### Configuración de Firebase

Asegúrate de que las reglas de Firebase Realtime Database permitan acceso autenticado:

```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

## 📁 Estructura del Proyecto

```
web/
├── main.py                          # Aplicación principal
├── config.py                        # Configuración y constantes
├── firebase_manager.py              # Gestión de Firebase
├── ark_api.py                       # Cliente API de ARK Status
├── components/
│   ├── login_view.py               # Vista de login
│   ├── sidebar.py                  # Barra lateral de navegación
│   ├── server_status_view.py       # Vista de estado del servidor
│   ├── generators_view.py          # Vista de generadores
│   ├── tasks_view.py               # Vista de tareas
│   └── members_view.py             # Vista de miembros
├── requirements.txt                 # Dependencias Python
├── Dockerfile                       # Configuración Docker
├── .dockerignore                   # Archivos ignorados por Docker
└── README.md                        # Este archivo
```

## 🎨 Diseño

- **Tema**: Dark Mode premium (#0f0f0f fondo, #1a1a1a tarjetas)
- **Acento**: Cyan (#00d4ff)
- **Tipografía**: Segoe UI
- **Componentes**: Material Design con Flet

## 🔧 Tecnologías

- **Frontend**: Flet (Python UI Framework)
- **Backend**: Firebase Realtime Database
- **API Externa**: ARK Status API
- **Deployment**: Google Cloud Run
- **Containerización**: Docker

## 📝 Uso

1. **Login**: Ingresar con credenciales de Firebase
2. **Seleccionar Roles**: Marcar roles activos en la barra lateral
3. **Navegar**: Usar los botones de la barra lateral para cambiar de sección
4. **Gestionar Datos**: Añadir, editar o eliminar generadores, tareas y miembros

## 🔒 Seguridad

- Todas las operaciones requieren autenticación
- Los tokens de Firebase se manejan de forma segura
- Las credenciales de API están en variables de entorno (recomendado para producción)

## 📊 Monitoreo

- **Heartbeat**: Actualización cada 30 segundos
- **Server Status**: Actualización cada 50 segundos
- **Generadores**: Actualización cada 60 segundos

## 🤝 Contribuciones

Este es un proyecto privado para la tribu FOG de ARK.

## 📄 Licencia

Uso privado - FOG Tribe © 2026
