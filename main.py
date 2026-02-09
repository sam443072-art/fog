# main.py
# Aplicación principal de ARK Tribe Manager

import flet as ft
import os
import sys

# Asegurar que el directorio actual esté en el path (para Render/Railway)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firebase_manager import FirebaseManager
from ark_api import ARKStatusAPI
from components.login_view import LoginView
from components.sidebar import Sidebar
from components.server_status_view import ServerStatusView
from components.generators_view import GeneratorsView
from components.tasks_view import TasksView
from components.members_view import MembersView
from config import (
    COLORS, 
    SERVER_UPDATE_INTERVAL, 
    HEARTBEAT_INTERVAL, 
    GENERATOR_UPDATE_INTERVAL
)
import asyncio


class ARKTribeManager:
    """Aplicación principal de gestión de tribu ARK"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.firebase = FirebaseManager()
        self.ark_api = ARKStatusAPI()
        
        # Vistas
        self.login_view = None
        self.sidebar = None
        self.server_status_view = None
        self.generators_view = None
        self.tasks_view = None
        self.members_view = None
        
        # Contenedores principales
        self.main_layout = None
        self.content_container = None
        
        # Estado
        self.current_section = "server"
        self.current_roles = []
        self.is_running = True
        
        # Timers
        self.heartbeat_task = None
        self.server_update_task = None
        self.generator_update_task = None
        
        self._setup_page()
        self._show_login()
    
    def _setup_page(self):
        """Configurar página principal"""
        self.page.title = "ARK Tribe Manager - FOG"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = COLORS["background"]
        self.page.padding = 0
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.window_min_width = 1200
        self.page.window_min_height = 700
        
        # Configurar tema personalizado
        self.page.theme = ft.Theme(
            color_scheme_seed=COLORS["accent"],
            font_family="Segoe UI"
        )
        
        # Evento de cambio de tamaño
        self.page.on_resize = self._handle_resize
    
    def _show_login(self):
        """Mostrar vista de login"""
        self.login_view = LoginView(on_login_success=self._handle_login)
        self.page.controls.clear()
        self.page.add(self.login_view.build())
        self.page.update()
    
    def _handle_login(self, email: str, password: str):
        """Manejar intento de login"""
        success, message = self.firebase.login(email, password)
        
        if success:
            self._show_main_app()
            self._start_background_tasks()
        else:
            self.login_view.show_error(message)
    
    def _show_main_app(self):
        """Mostrar aplicación principal"""
        # Crear sidebar
        self.sidebar = Sidebar(
            on_section_change=self._handle_section_change,
            on_roles_change=self._handle_roles_change,
            on_logout=self._handle_logout,
            username=self.firebase.user_email
        )
        
        # Crear vistas de secciones
        self.server_status_view = ServerStatusView()
        self.generators_view = GeneratorsView(self.firebase)
        self.tasks_view = TasksView(self.firebase)
        self.members_view = MembersView(self.firebase)
        
        # Contenedor de contenido
        self.content_container = ft.Container(
            content=self.server_status_view.build(),
            expand=True,
            bgcolor=COLORS["background"]
        )
        
        # Layout principal (será dinámico)
        self.main_layout = ft.Container(expand=True)
        self._update_layout()
        
        self.page.controls.clear()
        self.page.add(self.main_layout)
        self.page.update()
        
        # Cargar datos iniciales
        self._refresh_current_section()
    
    def _handle_resize(self, e):
        """Manejar cambio de tamaño de ventana"""
        if self.sidebar: # Solo si ya estamos dentro de la app
            self._update_layout()
            self.page.update()

    def _update_layout(self):
        """Actualizar el layout basado en el ancho de pantalla"""
        if not self.sidebar:
            return

        is_mobile = self.page.width < 800
        
        # Reset sidebar build
        sidebar_content = self.sidebar.build()
        
        if is_mobile:
            # En móvil usamos un Drawer
            self.page.drawer = ft.NavigationDrawer(
                controls=[sidebar_content],
                bgcolor=COLORS["card"]
            )
            
            # Botón de menú (Hamburger)
            menu_button = ft.IconButton(
                icon=ft.Icons.MENU,
                icon_color=COLORS["accent"],
                on_click=lambda _: self.page.show_drawer(self.page.drawer)
            )
            
            header_mobile = ft.Container(
                content=ft.Row([
                    menu_button,
                    ft.Text("ARK MANAGER", size=18, weight=ft.FontWeight.BOLD, color=COLORS["accent"]),
                ], alignment=ft.MainAxisAlignment.START),
                padding=10,
                bgcolor=COLORS["card"],
                border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"]))
            )
            
            # En móvil, el contenedor de contenido NO debe tener expand=True en el sentido vertical
            # para que el scroll del main_layout funcione bien.
            self.content_container.expand = False
            
            self.main_layout.content = ft.Column([
                header_mobile,
                self.content_container
            ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
            
        else:
            # En desktop, quitamos el drawer
            self.page.drawer = None
            self.content_container.expand = True
            sidebar_content.width = 250
            
            self.main_layout.content = ft.Row([
                sidebar_content,
                self.content_container
            ], spacing=0, expand=True)
    
    def _handle_section_change(self, section: str):
        """Cambiar sección activa"""
        self.current_section = section
        
        # Cerrar el drawer en móvil si está abierto
        if self.page.drawer and self.page.drawer.open:
            self.page.drawer.open = False
            self.page.update()
            
        # Actualizar contenido
        if section == "server":
            self.content_container.content = self.server_status_view.build()
            self._update_server_status()
        elif section == "generators":
            self.content_container.content = self.generators_view.build()
            self.generators_view.refresh_generators(self.page)
        elif section == "tasks":
            self.content_container.content = self.tasks_view.build()
            self.tasks_view.refresh_tasks(self.page)
        elif section == "members":
            self.content_container.content = self.members_view.build()
            self.members_view.refresh_members(self.page)
        
        self.page.update()
    
    def _handle_roles_change(self, roles: list):
        """Actualizar roles seleccionados"""
        self.current_roles = roles
        # El heartbeat se actualizará automáticamente en el próximo ciclo
    
    def _handle_logout(self):
        """Cerrar sesión"""
        self.is_running = False
        self.firebase.logout()
        # Limpiar referencias a vistas
        self.sidebar = None
        self.server_status_view = None
        self.generators_view = None
        self.tasks_view = None
        self.members_view = None
        self._show_login()
    
    def _refresh_current_section(self):
        """Refrescar datos de la sección actual"""
        if self.current_section == "server":
            self._update_server_status()
        elif self.current_section == "generators":
            if self.generators_view:
                self.generators_view.refresh_generators(self.page)
        elif self.current_section == "tasks":
            if self.tasks_view:
                self.tasks_view.refresh_tasks(self.page)
        elif self.current_section == "members":
            if self.members_view:
                self.members_view.refresh_members(self.page)
    
    def _update_server_status(self):
        """Actualizar estado del servidor"""
        if self.server_status_view:
            server_data = self.ark_api.get_server_status()
            self.server_status_view.update_server_data(server_data, self.page)
    
    def _update_active_admins(self):
        """Actualizar lista de admins activos"""
        if self.sidebar:
            active_admins = self.firebase.get_active_admins()
            self.sidebar.update_active_admins(active_admins, self.page)
    
    def _start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        self.is_running = True
        
        # Crear tasks asíncronos
        asyncio.create_task(self._heartbeat_loop())
        asyncio.create_task(self._server_update_loop())
        asyncio.create_task(self._generator_update_loop())
    
    async def _heartbeat_loop(self):
        """Loop de heartbeat (30 segundos)"""
        while self.is_running:
            try:
                self.firebase.update_heartbeat(self.current_roles)
                self._update_active_admins()
            except Exception as e:
                print(f"Error en heartbeat: {e}")
            
            await asyncio.sleep(HEARTBEAT_INTERVAL / 1000)
    
    async def _server_update_loop(self):
        """Loop de actualización del servidor (50 segundos)"""
        while self.is_running:
            try:
                if self.current_section == "server":
                    self._update_server_status()
            except Exception as e:
                print(f"Error actualizando servidor: {e}")
            
            await asyncio.sleep(SERVER_UPDATE_INTERVAL / 1000)
    
    async def _generator_update_loop(self):
        """Loop de actualización de generadores (60 segundos)"""
        while self.is_running:
            try:
                if self.current_section == "generators" and self.generators_view:
                    self.generators_view.refresh_generators(self.page)
            except Exception as e:
                print(f"Error actualizando generadores: {e}")
            
            await asyncio.sleep(GENERATOR_UPDATE_INTERVAL / 1000)


def main(page: ft.Page):
    """Función principal de Flet"""
    ARKTribeManager(page)


if __name__ == "__main__":
    import os
    # Detectar puerto de Railway o usar 8080 por defecto
    port = int(os.environ.get("PORT", 8080))
    
    # En producción (Railway/Render/Docker), usar modo servidor puro (sin intentar abrir navegador local)
    if os.environ.get("PORT"):
        print(f"🚀 Iniciando servidor en puerto {port}...")
        try:
            ft.app(target=main, port=port, host="0.0.0.0")
        except Exception as e:
            print(f"❌ ERROR CRÍTICO AL INICIAR APP: {e}")
    else:
        # Para desarrollo local (ventana nativa)
        ft.app(target=main)
