# components/members_view.py
# Vista de gestión de miembros

import flet as ft
from config import COLORS, ROLE_TAGS
from typing import Dict, Any


class MembersView:
    """Vista de gestión de miembros de la tribu"""
    
    def __init__(self, firebase_manager):
        self.firebase = firebase_manager
        self.page = None
        
        # Inicializar todos los controles en __init__ para asegurar que existan
        self.name_field = ft.TextField(
            label="Nombre Ark",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            expand=True
        )
        
        self.discord_field = ft.TextField(
            label="Usuario Discord",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            expand=True
        )
        
        self.vouch_field = ft.TextField(
            label="Vouch",
            hint_text="Quien lo trajo",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            expand=True
        )
        
        self.trust_dropdown = ft.Dropdown(
            label="Nivel de Confianza",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            options=[
                ft.dropdown.Option("high", "Alta (Verde)"),
                ft.dropdown.Option("medium", "Media (Naranja)"),
                ft.dropdown.Option("low", "Baja (Rojo)"),
            ],
            value="medium"
        )
        
        # Checkboxes de roles
        self.role_checkboxes = {
            "ADMIN": ft.Checkbox(label="ADMIN", value=False, fill_color=ROLE_TAGS["ADMIN"]["color"]),
            "builder": ft.Checkbox(label="Builder", value=False, fill_color=ROLE_TAGS["builder"]["color"]),
            "GH": ft.Checkbox(label="GH", value=False, fill_color=ROLE_TAGS["GH"]["color"]),
            "BR": ft.Checkbox(label="BR", value=False, fill_color=ROLE_TAGS["BR"]["color"]),
        }
        
        self.members_container = ft.Column([], spacing=10)
        self.error_text = ft.Text("", color=COLORS["danger"], size=12)

    def build(self) -> ft.Container:
        """Construir vista de miembros"""
        
        # Header
        header = ft.Text(
            "Miembros de la Tribu",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=COLORS["text_primary"]
        )
        
        roles_section = ft.Container(
            content=ft.Column([
                ft.Text("Roles", size=12, color=COLORS["text_secondary"]),
                ft.Row([
                    self.role_checkboxes["ADMIN"],
                    self.role_checkboxes["builder"],
                    self.role_checkboxes["GH"],
                    self.role_checkboxes["BR"],
                ], spacing=10, wrap=True)
            ], spacing=5),
        )
        
        add_button = ft.ElevatedButton(
            content=ft.Text("Añadir Miembro"),
            bgcolor=COLORS["accent"],
            color="#000000",
            height=40,
            on_click=lambda _: self._add_member()
        )
        
        add_form = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.name_field,
                    self.discord_field,
                    self.vouch_field,
                    self.trust_dropdown
                ], spacing=15, wrap=True),
                roles_section,
                self.error_text,
                add_button
            ], spacing=15),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        members_list = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Lista de Miembros",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_secondary"]
                ),
                self.members_container
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
                members_list
            ], spacing=20),
            padding=30
        )
    
    def _add_member(self):
        """Añadir nuevo miembro"""
        # Limpiar error anterior
        self.error_text.value = ""
        
        name = self.name_field.value
        discord = self.discord_field.value
        vouch = self.vouch_field.value
        trust = self.trust_dropdown.value
        
        if not name or not discord or not vouch:
            self.error_text.value = "Por favor completa los campos Nombre, Discord y Vouch."
            if self.page: self.page.update()
            return
        
        # Obtener roles seleccionados
        roles = [role for role, checkbox in self.role_checkboxes.items() if checkbox.value]
        
        success = self.firebase.add_member(name, discord, vouch, trust, roles)
        if success:
            self.name_field.value = ""
            self.discord_field.value = ""
            self.vouch_field.value = ""
            self.trust_dropdown.value = "medium"
            for checkbox in self.role_checkboxes.values():
                checkbox.value = False
            
            if self.page:
                self.page.update()
            self.refresh_members(self.page)
        else:
            self.error_text.value = "Error al conectar con la base de datos."
            if self.page: self.page.update()
    
    def refresh_members(self, page=None):
        """Actualizar lista de miembros"""
        if page:
            self.page = page
        
        members = self.firebase.get_members()
        self.members_container.controls.clear()
        
        if not members:
            self.members_container.controls.append(
                ft.Text("No hay miembros registrados", size=14, color=COLORS["text_secondary"])
            )
        else:
            for member_id, member_data in members.items():
                self.members_container.controls.append(
                    self._create_member_card(member_id, member_data)
                )
        
        if self.page:
            self.page.update()
    
    def _create_member_card(self, member_id: str, member_data: Dict[str, Any]) -> ft.Container:
        """Crear tarjeta de miembro"""
        name = member_data.get("name", "Unknown")
        discord = member_data.get("discord", "-")
        roles = member_data.get("roles", [])
        trust = member_data.get("trust_level", "medium")
        vouch = member_data.get("vouch", "None")
        
        # Color según confianza
        trust_colors = {
            "high": COLORS["success"],
            "medium": COLORS["warning"],
            "low": COLORS["danger"]
        }
        trust_color = trust_colors.get(trust, COLORS["text_secondary"])
        
        # Badges de roles
        role_badges = []
        for role in roles:
            role_info = ROLE_TAGS.get(role, {"color": COLORS["text_secondary"], "label": role})
            role_badges.append(
                ft.Container(
                    content=ft.Text(role_info["label"], size=10, color="#000000", weight=ft.FontWeight.BOLD),
                    bgcolor=role_info["color"],
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    border_radius=4
                )
            )
        
        return ft.Container(
            content=ft.Row([
                ft.Container(width=5, bgcolor=trust_color, border_radius=2), # Barra lateral de confianza
                ft.Column([
                    ft.Row([
                        ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color=COLORS["text_primary"]),
                        ft.Text(f"(@{discord})", size=12, color=COLORS["text_secondary"]),
                    ], spacing=10),
                    ft.Text(f"Vouch: {vouch}", size=11, color=COLORS["text_secondary"]),
                    ft.Row(role_badges, spacing=5) if role_badges else ft.Container()
                ], spacing=5, expand=True),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=COLORS["danger"],
                    on_click=lambda _, mid=member_id: self._delete_member(mid)
                )
            ], spacing=15),
            padding=15,
            bgcolor=COLORS["card_hover"],
            border_radius=8,
            border=ft.border.all(1, COLORS["border"])
        )
    
    def _delete_member(self, member_id: str):
        """Eliminar un miembro"""
        self.firebase.delete_member(member_id)
        self.refresh_members(self.page)
