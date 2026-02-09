# run_web.py
# Script para ejecutar la aplicación en modo web (navegador)

import flet as ft
from main import main

if __name__ == "__main__":
    print("=" * 50)
    print("  ARK Tribe Manager - Modo Web")
    print("=" * 50)
    print("\nIniciando servidor web...")
    print("Abre tu navegador en: http://localhost:8080\n")
    
    # Ejecutar en modo web
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=8080,
        host="127.0.0.1"
    )
