# Guía de Despliegue en Railway - ARK Tribe Manager

Sigue estos pasos para desplegar tu aplicación en **Railway.app**:

### 1. Preparación

La aplicación ya está configurada con un `Dockerfile` y `railway.json`.

### 2. Pasos en Railway

1. Sube tu código a un repositorio de **GitHub**.
2. Entra en [Railway.app](https://railway.app/) y crea un **New Project**.
3. Selecciona **Deploy from GitHub repo** y elige tu repositorio.
4. Railway detectará automáticamente el `Dockerfile`.

### 3. Variables de Entorno (IMPORTANTE)

Para que la aplicación funcione y sea segura, debes configurar las siguientes variables en la pestaña **Variables** de Railway:

| Variable                  | Valor                                                       |
| :------------------------ | :---------------------------------------------------------- |
| `FIREBASE_API_KEY`        | Tu API Key de Firebase                                      |
| `FIREBASE_AUTH_DOMAIN`    | `fog-astra.firebaseapp.com`                                 |
| `FIREBASE_DB_URL`         | `https://fog-astra-default-rtdb.firebaseio.com`             |
| `FIREBASE_PROJECT_ID`     | `fog-astra`                                                 |
| `FIREBASE_STORAGE_BUCKET` | `fog-astra.firebasestorage.app`                             |
| `FIREBASE_MESSAGING_ID`   | `503068814140`                                              |
| `FIREBASE_APP_ID`         | `1:503068814140:web:db5ff6833b7dc553144c39`                 |
| `DISCORD_WEBHOOK`         | Tu URL de Webhook de Discord                                |
| `ARKSTATUS_API_KEY`       | Tu API Key de arkstatus.com                                 |
| `ARK_SERVER_ID`           | `68116671`                                                  |
| `PORT`                    | `8080` (Railway lo suele asignar solo, pero puedes ponerlo) |

### 4. Dominio

Una vez desplegado, Railway te dará una URL (ej: `web-production.up.railway.app`). Los admins podrán entrar desde cualquier navegador.

### Notas de Solución de Problemas

- Si ves errores de **"solo se permite un uso de cada dirección de socket"**, es porque intentaste abrir el modo web localmente dos veces. Cierra todas las terminales y usa solo `run_web.py`.
- En Railway, la aplicación siempre correrá en modo **Web Browser**.
