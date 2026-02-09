# components/sidebar.py
# Barra lateral de navegación con selector de roles

import flet as ft
from config import COLORS, ROLE_TAGS


class Sidebar:
    """Barra lateral de navegación con roles y admins activos"""
    
    def __init__(self, on_section_change, on_roles_change, on_logout, username: str):
        self.on_section_change = on_section_change
        self.on_roles_change = on_roles_change
        self.on_logout = on_logout
        self.username = username
        self.current_section = "server"
        self.selected_roles = []
        self.active_admins_container = None
        self.role_checkboxes = {}
        self.page = None
    
    def build(self) -> ft.Container:
        """Construir sidebar"""
        
        # Logo/Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "FOG TRIBE",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["accent"]
                ),
                ft.Text(
                    f"@{self.username}",
                    size=12,
                    color=COLORS["text_secondary"]
                ),
            ], spacing=5),
            padding=20,
            border=ft.border.only(bottom=ft.BorderSide(1, COLORS["border"]))
        )
        
        # Botones de navegación
        nav_buttons = ft.Column([
            self._create_nav_button("Server Status", "server", ft.Icons.CLOUD),
            self._create_nav_button("Generadores", "generators", ft.Icons.POWER),
            self._create_nav_button("Tareas", "tasks", ft.Icons.TASK_ALT),
            self._create_nav_button("Miembros", "members", ft.Icons.PEOPLE),
        ], spacing=5)
        
        # Selector de roles
        roles_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Mis Roles",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_secondary"]
                ),
                ft.Column([
                    self._create_role_checkbox("ADMIN"),
                    self._create_role_checkbox("builder"),
                    self._create_role_checkbox("GH"),
                    self._create_role_checkbox("BR"),
                ], spacing=8)
            ], spacing=10),
            padding=20,
            border=ft.border.only(
                top=ft.BorderSide(1, COLORS["border"]),
                bottom=ft.BorderSide(1, COLORS["border"])
            )
        )
        
        # Admins activos
        self.active_admins_container = ft.Column([], spacing=8)
        
        admins_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Admins Activos",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_secondary"]
                ),
                self.active_admins_container
            ], spacing=10),
            padding=20,
        )
        
        # Botón de logout
        logout_button = ft.Container(
            content=ft.TextButton(
                content=ft.Text("Cerrar Sesión"),
                icon=ft.Icons.LOGOUT,
                style=ft.ButtonStyle(
                    color=COLORS["danger"]
                ),
                on_click=lambda _: self.on_logout()
            ),
            padding=ft.padding.only(left=20, right=20, bottom=20)
        )
        
        # Contenedor principal
        sidebar_container = ft.Container(
            content=ft.Column([
                header,
                nav_buttons,
                roles_section,
                ft.Container(expand=True),  # Spacer
                admins_section,
                logout_button
            ], spacing=0),
            bgcolor=COLORS["card"],
            border=ft.border.only(right=ft.BorderSide(1, COLORS["border"]))
        )
        
        return sidebar_container
    
    def _create_nav_button(self, text: str, section: str, icon) -> ft.Container:
        """Crear botón de navegación"""
        is_selected = self.current_section == section
        
        button = ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=20, color=COLORS["accent"] if is_selected else COLORS["text_secondary"]),
                ft.Text(
                    text,
                    size=14,
                    color=COLORS["accent"] if is_selected else COLORS["text_primary"],
                    weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
                )
            ], spacing=10),
            padding=15,
            margin=ft.margin.symmetric(horizontal=10),
            bgcolor=COLORS["card_hover"] if is_selected else "transparent",
            border_radius=8,
            border=ft.border.all(1, COLORS["accent"] if is_selected else "transparent"),
            on_click=lambda _, s=section: self._handle_section_change(s),
            ink=True
        )
        
        return button
    
    def _create_role_checkbox(self, role: str) -> ft.Checkbox:
        """Crear checkbox de rol"""
        role_info = ROLE_TAGS.get(role, {"color": COLORS["text_secondary"], "label": role})
        
        checkbox = ft.Checkbox(
            label=role_info["label"],
            value=False,
            fill_color=role_info["color"],
            check_color="#000000",
            label_style=ft.TextStyle(color=COLORS["text_primary"], size=13),
            on_change=lambda _: self._handle_roles_change()
        )
        
        self.role_checkboxes[role] = checkbox
        return checkbox
    
    def _handle_section_change(self, section: str):
        """Cambiar sección activa"""
        self.current_section = section
        self.on_section_change(section)
    
    def _handle_roles_change(self):
        """Actualizar roles seleccionados"""
        self.selected_roles = [
            role for role, checkbox in self.role_checkboxes.items()
            if checkbox.value
        ]
        self.on_roles_change(self.selected_roles)
    
    def update_active_admins(self, admins: dict, page=None):
        """Actualizar lista de admins activos"""
        if page:
            self.page = page
            
        self.active_admins_container.controls.clear()
        
        if not admins:
            self.active_admins_container.controls.append(
                ft.Text("Ninguno", size=12, color=COLORS["text_secondary"])
            )
        else:
            for admin_id, admin_data in admins.items():
                is_active = admin_data.get("active", False)
                roles = admin_data.get("roles", [])
                
                # Crear badges de roles
                role_badges = []
                for role in roles:
                    role_info = ROLE_TAGS.get(role, {"color": COLORS["text_secondary"], "label": role})
                    role_badges.append(
                        ft.Container(
                            content=ft.Text(role_info["label"], size=9, color="#000000"),
                            bgcolor=role_info["color"],
                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            border_radius=4
                        )
                    )
                
                admin_item = ft.Row([
                    ft.Container(
                        width=8,
                        height=8,
                        bgcolor=COLORS["success"] if is_active else COLORS["text_secondary"],
                        border_radius=4
                    ),
                    ft.Column([
                        ft.Text(admin_id, size=12, color=COLORS["text_primary"]),
                        ft.Row(role_badges, spacing=4) if role_badges else ft.Container()
                    ], spacing=4, expand=True)
                ], spacing=8)
                
                self.active_admins_container.controls.append(admin_item)
        
        if self.page:
            self.page.update()
