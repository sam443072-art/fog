# components/server_status_view.py
# Vista del estado del servidor ARK

import flet as ft
from config import COLORS
from typing import Optional, Dict, Any


class ServerStatusView:
    """Vista del estado del servidor con información en tiempo real"""
    
    def __init__(self):
        self.server_data = None
        self.name_text = None
        self.map_text = None
        self.players_text = None
        self.players_progress = None
        self.rank_text = None
        self.ping_text = None
        self.version_text = None
        self.uptime_text = None
        self.peak_text = None
        self.platform_text = None
        self.status_indicator = None
        self.page = None
    
    def build(self) -> ft.Container:
        """Construir vista de server status"""
        
        # Indicador de estado
        self.status_indicator = ft.Container(
            width=12,
            height=12,
            bgcolor=COLORS["text_secondary"],
            border_radius=6
        )
        
        # Título con indicador
        header = ft.Row([
            ft.Text(
                "Server Status",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=COLORS["text_primary"]
            ),
            self.status_indicator
        ], spacing=15)
        
        # Información principal
        self.name_text = ft.Text("Cargando...", size=20, weight=ft.FontWeight.BOLD, color=COLORS["accent"])
        self.map_text = ft.Text("Map: -", size=14, color=COLORS["text_secondary"])
        
        main_info = ft.Container(
            content=ft.Column([
                self.name_text,
                self.map_text
            ], spacing=5),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        # Estadísticas principales
        self.players_text = ft.Text("0", size=24, weight=ft.FontWeight.BOLD, color=COLORS["accent"])
        self.rank_text = ft.Text("-", size=24, weight=ft.FontWeight.BOLD, color=COLORS["accent"])
        self.ping_text = ft.Text("-", size=24, weight=ft.FontWeight.BOLD, color=COLORS["accent"])
        self.version_text = ft.Text("-", size=14, weight=ft.FontWeight.BOLD, color=COLORS["accent"])
        
        # Grid de estadísticas (Responsivo)
        stats_grid = ft.ResponsiveRow([
            self._create_stat_card("Players Online", self.players_text, 6),
            self._create_stat_card("Server Rank", self.rank_text, 6),
            self._create_stat_card("Ping", self.ping_text, 6),
            self._create_stat_card("Version", self.version_text, 6),
        ], spacing=20)
        
        # Stats adicionales
        self.uptime_text = ft.Text("-", size=14, color=COLORS["text_primary"])
        self.peak_text = ft.Text("-", size=14, color=COLORS["text_primary"])
        self.platform_text = ft.Text("-", size=14, color=COLORS["text_primary"])
        
        extra_stats = ft.Container(
            content=ft.Column([
                ft.Text("Información Adicional", size=16, weight=ft.FontWeight.BOLD, color=COLORS["text_secondary"]),
                ft.Divider(color=COLORS["border"], height=1),
                self._create_info_row("Uptime", self.uptime_text),
                self._create_info_row("Peak Players", self.peak_text),
                self._create_info_row("Platform", self.platform_text),
            ], spacing=10),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        # Contenedor principal
        return ft.Container(
            content=ft.Column([
                header,
                main_info,
                stats_grid,
                extra_stats
            ], spacing=20),
            padding=30
        )
    
    def _create_stat_card(self, title: str, content, col: int = 3) -> ft.Container:
        """Crear tarjeta de estadística"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=12, color=COLORS["text_secondary"], weight=ft.FontWeight.BOLD),
                content
            ], spacing=10),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"]),
            col={"sm": 6, "md": col}
        )
    
    def _create_info_row(self, label: str, value_widget) -> ft.Row:
        """Crear fila de información"""
        return ft.Row([
            ft.Text(f"{label}:", size=14, color=COLORS["text_secondary"], width=120),
            value_widget
        ], spacing=10)
    
    def update_server_data(self, data: Optional[Dict[str, Any]], page=None):
        """Actualizar datos del servidor"""
        if page:
            self.page = page
            
        if not data:
            self._show_offline()
            return
        
        self.server_data = data
        
        # Actualizar estado
        is_online = data.get("online", False)
        self.status_indicator.bgcolor = COLORS["success"] if is_online else COLORS["danger"]
        
        # Actualizar información principal
        self.name_text.value = data.get("name", "Unknown Server")
        self.map_text.value = f"Map: {data.get('map', 'Unknown')}"
        
        # Actualizar jugadores
        players = data.get("players", 0)
        max_players = data.get("max_players", 70)
        self.players_text.value = f"{players} / {max_players}"
        self.players_progress.value = players / max_players if max_players > 0 else 0
        
        # Actualizar ping
        ping = data.get("ping", 0)
        self.ping_text.value = f"{ping} ms"
        
        # Actualizar versión
        self.version_text.value = data.get("version", "N/A")
        
        # Actualizar stats adicionales
        uptime = data.get("uptime", 0)
        self.uptime_text.value = self._format_uptime(uptime)
        self.peak_text.value = str(data.get("peak_players", 0))
        self.platform_text.value = data.get("platform", "N/A")
        
        if self.page:
            self.page.update()
    
    def _show_offline(self):
        """Mostrar estado offline"""
        if self.status_indicator:
            self.status_indicator.bgcolor = COLORS["danger"]
        
        if self.name_text:
            self.name_text.value = "Servidor Offline"
            
        if self.page:
            self.page.update()
    
    def _format_uptime(self, seconds: int) -> str:
        """Formatear uptime en formato legible"""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m"
        elif seconds < 86400:
            return f"{seconds // 3600}h"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            return f"{days}d {hours}h"
