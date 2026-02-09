import os

# Configuración de Firebase y servicios externos
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyB0wOU6YlaYB3NWr9Pfkb6u92zt4jBaooE"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "fog-astra.firebaseapp.com"),
    "databaseURL": os.getenv("FIREBASE_DB_URL", "https://fog-astra-default-rtdb.firebaseio.com"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", "fog-astra"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "fog-astra.firebasestorage.app"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_ID", "503068814140"),
    "appId": os.getenv("FIREBASE_APP_ID", "1:503068814140:web:db5ff6833b7dc553144c39")
}

# Discord Webhook para alertas
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1445205056017404014/utT7gv4dQm-2Erzb4NLNhctI33ftk9qbNAybBsWL1NtyBXorAzZMzabchfQ-zLLg0U-N")

# ARK Server Status API
ARKSTATUS_API_KEY = os.getenv("ARKSTATUS_API_KEY", "ark_aa23ee3a531fd4d5926adb70ec7aa9c23ca22d6e85d3b47fe78316445d14e154")
ARKSTATUS_URL = "https://arkstatus.com/api/v1/servers"
ARK_SERVER_ID = os.getenv("ARK_SERVER_ID", "68116671")  # ID del servidor en arkstatus.com

# Configuración de actualización
SERVER_UPDATE_INTERVAL = 50000  # 50 segundos (para respetar límite de API)
HEARTBEAT_INTERVAL = 30000  # 30 segundos
GENERATOR_UPDATE_INTERVAL = 60000  # 1 minuto
ADMIN_TIMEOUT = 120  # 2 minutos para considerar admin inactivo

# Colores del tema
COLORS = {
    "background": "#0f0f0f",
    "card": "#1a1a1a",
    "card_hover": "#222222",
    "accent": "#00d4ff",
    "accent_hover": "#00b8e6",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "border": "#2a2a2a",
    "success": "#00ff88",
    "warning": "#ffaa00",
    "danger": "#ff4444",
    "trust_high": "#00ff88",
    "trust_medium": "#ffaa00",
    "trust_low": "#ff4444",
}

# Tags de roles
ROLE_TAGS = {
    "ADMIN": {"color": "#ff0066", "label": "ADMIN"},
    "builder": {"color": "#00d4ff", "label": "Builder"},
    "GH": {"color": "#00ff88", "label": "Greenhouse"},
    "BR": {"color": "#ffaa00", "label": "Breeder"},
}
