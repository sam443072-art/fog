# components/generators_view.py
# Vista de gestión de generadores con countdown

import flet as ft
from config import COLORS
import time
from typing import Dict, Any


class GeneratorsView:
    """Vista de generadores con cuenta regresiva en tiempo real"""
    
    def __init__(self, firebase_manager):
        self.firebase = firebase_manager
        self.generators_container = None
        self.name_field = None
        self.duration_field = None
        self.page = None
    
    def build(self) -> ft.Container:
        """Construir vista de generadores"""
        
        # Header
        header = ft.Text(
            "Generadores",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=COLORS["text_primary"]
        )
        
        # Formulario para añadir generador
        self.name_field = ft.TextField(
            label="Nombre del Generador",
            hint_text="Gen Principal",
            width=250,
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14
        )
        
        self.duration_field = ft.TextField(
            label="Duración (días)",
            hint_text="7",
            width=150,
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        add_button = ft.ElevatedButton(
            content=ft.Text("Añadir Generador"),
            bgcolor=COLORS["accent"],
            color="#000000",
            height=40,
            on_click=lambda _: self._add_generator()
        )
        
        add_form = ft.Container(
            content=ft.Row([
                self.name_field,
                self.duration_field,
                add_button
            ], spacing=15, wrap=True),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        # Contenedor de generadores
        self.generators_container = ft.Column([], spacing=10)
        
        generators_list = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Generadores Activos",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_secondary"]
                ),
                self.generators_container
            ], spacing=15),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        # Contenedor principal
        return ft.Container(
            content=ft.Column([
                header,
                add_form,
                generators_list
            ], spacing=20),
            padding=30
        )
    
    def _add_generator(self):
        """Añadir nuevo generador"""
        name = self.name_field.value
        duration_str = self.duration_field.value
        
        if not name or not duration_str:
            return
        
        try:
            duration_days = int(duration_str)
            if duration_days <= 0:
                return
            
            success = self.firebase.add_generator(name, duration_days)
            if success:
                self.name_field.value = ""
                self.duration_field.value = ""
                if self.page:
                    self.page.update()
                self.refresh_generators(self.page)
        except ValueError:
            pass
    
    def refresh_generators(self, page=None):
        """Actualizar lista de generadores"""
        if page:
            self.page = page
        
        generators = self.firebase.get_generators()
        self.generators_container.controls.clear()
        
        if not generators:
            self.generators_container.controls.append(
                ft.Text("No hay generadores activos", size=14, color=COLORS["text_secondary"])
            )
        else:
            for gen_id, gen_data in generators.items():
                self.generators_container.controls.append(
                    self._create_generator_card(gen_id, gen_data)
                )
        
        if self.page:
            self.page.update()
    
    def _create_generator_card(self, gen_id: str, gen_data: Dict[str, Any]) -> ft.Container:
        """Crear tarjeta de generador con countdown"""
        name = gen_data.get("name", "Sin nombre")
        start_time = gen_data.get("start_timestamp", 0)
        duration = gen_data.get("duration_seconds", 0)
        created_by = gen_data.get("created_by", "Unknown")
        
        # Calcular tiempo restante
        current_time = int(time.time())
        elapsed = current_time - start_time
        remaining = max(0, duration - elapsed)
        progress = 1 - (remaining / duration) if duration > 0 else 1
        
        # Formatear tiempo restante
        time_text = self._format_time(remaining)
        
        # Texto de tiempo
        countdown_text = ft.Text(
            time_text,
            size=16,
            weight=ft.FontWeight.BOLD,
            color=COLORS["accent"] if remaining > 0 else COLORS["danger"]
        )
        
        # Barra de progreso
        progress_bar = ft.ProgressBar(
            value=progress,
            width=None, # Quitar ancho fijo
            color=COLORS["warning"] if remaining > 0 else COLORS["danger"],
            bgcolor=COLORS["border"],
            height=8,
            border_radius=4
        )
        
        # Botón de eliminar
        delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=COLORS["danger"],
            tooltip="Eliminar",
            on_click=lambda _, gid=gen_id: self._delete_generator(gid)
        )
        
        return ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                    ft.Text(f"Por: {created_by}", size=11, color=COLORS["text_secondary"]),
                    countdown_text,
                    progress_bar
                ], spacing=8, expand=True),
                delete_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=15,
            bgcolor=COLORS["card_hover"],
            border_radius=8,
            border=ft.border.all(1, COLORS["border"])
        )
    
    def _delete_generator(self, gen_id: str):
        """Eliminar generador"""
        self.firebase.delete_generator(gen_id)
        self.refresh_generators(self.page)
    
    def _format_time(self, seconds: int) -> str:
        """Formatear tiempo en formato legible"""
        if seconds <= 0:
            return "EXPIRADO"
        
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
