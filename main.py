# main.py
# Aplicación principal de ARK Tribe Manager - Mobile Optimized

import flet as ft
import os
import sys
import asyncio
import time

# Asegurar que el directorio actual esté en el path
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

class ARKTribeManager:
    """Aplicación principal optimizada para Web y Móvil"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.firebase = FirebaseManager()
        self.ark_api = ARKStatusAPI()
        
        # Componentes
        self.login_view = None
        self.sidebar = None
        self.server_view = None
        self.generators_view = None
        self.tasks_view = None
        self.members_view = None
        
        # Estado
        self.current_section = "server"
        self.is_running = True
        
        # UI Elements
        self.content_container = ft.Container(expand=True, bgcolor=COLORS["background"])
        self.drawer = None
        self.app_bar = None
        
        self._setup_page()
        self._show_login()

    def _setup_page(self):
        self.page.title = "ARK Manager - FOG"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = COLORS["background"]
        self.page.padding = 0
        self.page.spacing = 0
        self.page.window_min_width = 350
        
        # Configurar tema Cyan Premium
        self.page.theme = ft.Theme(
            color_scheme_seed=COLORS["accent"],
            font_family="Segoe UI",
            visual_density=ft.VisualDensity.COMFORTABLE,
        )

    def _show_login(self):
        self.login_view = LoginView(
            firebase_manager=self.firebase,
            on_login_success=self._handle_login_success
        )
        self.login_view.page = self.page
        self.page.controls.clear()
        self.page.add(self.login_view.build())
        self.page.update()

    def _handle_login_success(self, email: str):
        self._init_app_components()
        self._setup_navigation()
        self._start_background_tasks()
        self._refresh_view()

    def _init_app_components(self):
        """Inicializar todos los componentes una sola vez"""
        self.sidebar = Sidebar(
            on_section_change=self._handle_section_change,
            on_roles_change=self._handle_roles_change,
            on_logout=self._handle_logout,
            username=self.firebase.user_email
        )
        self.sidebar.page = self.page
        
        self.server_view = ServerStatusView()
        self.generators_view = GeneratorsView(self.firebase)
        self.tasks_view = TasksView(self.firebase)
        self.members_view = MembersView(self.firebase)

    def _setup_navigation(self):
        """Configurar App Bar y Drawer móviles"""
        # Drawer (Menú lateral)
        self.page.drawer = ft.NavigationDrawer(
            controls=[self.sidebar.build_controls()],
            bgcolor=COLORS["card"]
        )
        
        # App Bar
        self.app_bar = ft.AppBar(
            leading=ft.IconButton(
                ft.Icons.MENU, 
                icon_color=COLORS["accent"], 
                on_click=lambda _: self._open_drawer()
            ),
            title=ft.Text("ARK MANAGER - FOG", size=18, weight=ft.FontWeight.BOLD, color=COLORS["accent"]),
            center_title=True,
            bgcolor=COLORS["card"],
            actions=[
                ft.IconButton(ft.Icons.REFRESH, icon_color=COLORS["text_secondary"], on_click=lambda _: self._refresh_current_data())
            ]
        )
        self.page.appbar = self.app_bar
        
        # Contenedor con Scroll
        self.scrollable_content = ft.Column(
            [self.content_container],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        self.page.controls.clear()
        self.page.add(self.scrollable_content)
        self.page.update()

    def _open_drawer(self):
        if self.page.drawer:
            self.page.drawer.open = True
            self.page.update()

    def _handle_section_change(self, section: str):
        self.current_section = section
        if self.page.drawer:
            self.page.drawer.open = False
            self.page.update()
        self._refresh_view()

    def _refresh_view(self):
        """Cambiar el contenido del contenedor principal"""
        if self.current_section == "server":
            self.content_container.content = self.server_view.build()
            self.server_view.page = self.page
            self._update_server_data()
        elif self.current_section == "generators":
            self.content_container.content = self.generators_view.build()
            self.generators_view.page = self.page
            self.generators_view.refresh_generators()
        elif self.current_section == "tasks":
            self.content_container.content = self.tasks_view.build()
            self.tasks_view.page = self.page
            self.tasks_view.refresh_tasks()
        elif self.current_section == "members":
            self.content_container.content = self.members_view.build()
            self.members_view.page = self.page
            self.members_view.refresh_members()
        
        self.page.update()

    def _handle_roles_change(self, roles: list):
        """Actualizar roles y forzar actualización inmediata de heartbeat"""
        asyncio.create_task(self._force_heartbeat(roles))

    async def _force_heartbeat(self, roles):
        self.firebase.update_heartbeat(roles)

    def _handle_logout(self):
        self.is_running = False
        self.firebase.logout()
        self.page.appbar = None
        self.page.drawer = None
        self._show_login()

    def _refresh_current_data(self):
        if self.current_section == "server": self._update_server_data()
        elif self.current_section == "generators": self.generators_view.refresh_generators()
        elif self.current_section == "tasks": self.tasks_view.refresh_tasks()
        elif self.current_section == "members": self.members_view.refresh_members()

    # ==================== BACKGROUND TASKS ====================
    
    def _start_background_tasks(self):
        asyncio.create_task(self._bg_server_update())
        asyncio.create_task(self._bg_heartbeat())
        asyncio.create_task(self._bg_generators_update())

    async def _bg_server_update(self):
        while self.is_running:
            if self.current_section == "server":
                self._update_server_data()
            await asyncio.sleep(SERVER_UPDATE_INTERVAL / 1000)

    async def _bg_heartbeat(self):
        while self.is_running:
            roles = self.sidebar.selected_roles if self.sidebar else []
            self.firebase.update_heartbeat(roles)
            
            # Actualizar lista de admins activos en el sidebar
            admins = self.firebase.get_active_admins()
            if self.sidebar:
                self.sidebar.update_active_admins(admins, self.page)
                
            await asyncio.sleep(HEARTBEAT_INTERVAL / 1000)

    async def _bg_generators_update(self):
        while self.is_running:
            if self.current_section == "generators":
                self.generators_view.refresh_generators()
            await asyncio.sleep(GENERATOR_UPDATE_INTERVAL / 1000)

    def _update_server_data(self):
        """Consultar API y actualizar vista de servidor"""
        # Ejecutar en hilo para no bloquear Flet
        asyncio.create_task(self._fetch_server_async())

    async def _fetch_server_async(self):
        data = await asyncio.to_thread(self.ark_api.get_server_status)
        if data and self.server_view:
            self.server_view.update_data(data, self.page)

async def main(page: ft.Page):
    app = ARKTribeManager(page)

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.getenv("PORT", 8502)))
