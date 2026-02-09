# QUICK_START.md

# Inicio Rápido - ARK Tribe Manager

## 🎯 Para Usuarios

### Opción 1: Acceder a la Aplicación Web (Recomendado)

Si la aplicación ya está desplegada en Cloud Run:

1. Abre tu navegador
2. Ve a la URL proporcionada (ej: `https://ark-tribe-manager-xxxxx.run.app`)
3. Inicia sesión con tus credenciales de Firebase
4. ¡Listo! Ya puedes gestionar tu tribu

### Opción 2: Ejecutar Localmente

**Requisitos:**

- Python 3.11 o superior
- pip instalado

**Pasos:**

1. Abre una terminal en la carpeta del proyecto

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:

   **Modo Ventana (Aplicación de Escritorio):**

   ```bash
   python run_local.py
   ```

   **Modo Web (Navegador):**

   ```bash
   python run_web.py
   ```

   Luego abre: http://localhost:8080

## 📱 Cómo Usar la Aplicación

### 1. Login

- Ingresa tu email y contraseña de Firebase
- Click en "Iniciar Sesión"

### 2. Seleccionar Roles

- En la barra lateral izquierda, marca tus roles activos:
  - ✅ ADMIN
  - ✅ Builder
  - ✅ GH (Greenhouse)
  - ✅ BR (Breeder)

### 3. Navegar por Secciones

#### 🌐 Server Status

- Ver estado del servidor en tiempo real
- Jugadores conectados
- Ping y versión
- Uptime y estadísticas

#### ⚡ Generadores

- **Añadir**: Nombre + Duración en días
- **Ver**: Countdown en tiempo real
- **Eliminar**: Click en el icono de basura

#### 📝 Tareas

- **Añadir**: Descripción + Tag (ADMIN/Builder/GH/BR)
- **Ver**: Lista de tareas activas con tags de colores
- **Eliminar**: Click en la X

#### 👥 Miembros

- **Añadir**: Nombre, Discord, Vouch, Nivel de Confianza, Roles
- **Ver**: Lista con indicadores de confianza (Verde/Naranja/Rojo)
- **Eliminar**: Click en el icono de basura

### 4. Admins Activos

- En la parte inferior de la barra lateral
- Muestra quién está conectado en tiempo real
- Actualización automática cada 30 segundos

## 🎨 Atajos y Tips

- **Colores de Confianza:**
  - 🟢 Verde = Alta confianza
  - 🟠 Naranja = Confianza media
  - 🔴 Rojo = Vigilar

- **Tags de Tareas:**
  - 🔴 ADMIN = Tareas administrativas
  - 🔵 Builder = Construcción
  - 🟢 GH = Greenhouse/Farming
  - 🟡 BR = Breeding

- **Generadores:**
  - La barra de progreso muestra el combustible restante
  - Cuando llega a 0, aparece "EXPIRADO" en rojo

## ❓ Preguntas Frecuentes

**P: ¿Cómo obtengo credenciales de Firebase?**
R: Contacta al administrador de la tribu.

**P: ¿Por qué no veo mis cambios?**
R: La aplicación se actualiza automáticamente. Si no ves cambios, refresca la página.

**P: ¿Puedo usar la app en móvil?**
R: Sí, la versión web es responsive y funciona en móviles.

**P: ¿Los datos se sincronizan en tiempo real?**
R: Sí, todos los cambios se reflejan automáticamente en Firebase.

**P: ¿Qué pasa si pierdo conexión?**
R: La app intentará reconectar automáticamente. Los cambios se guardarán cuando recuperes conexión.

## 🆘 Soporte

Si tienes problemas:

1. Verifica tu conexión a internet
2. Asegúrate de tener las credenciales correctas
3. Contacta al administrador del sistema

---

**¡Disfruta gestionando tu tribu ARK!** 🦖
