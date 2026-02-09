# components/login_view.py
# Vista de autenticación

import flet as ft
from config import COLORS


class LoginView:
    """Vista de login elegante con diseño premium"""
    
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.email_field = None
        self.password_field = None
        self.error_text = None
        self.login_button = None
    
    def build(self) -> ft.Container:
        """Construir vista de login"""
        
        # Campo de email
        self.email_field = ft.TextField(
            label="Email",
            bgcolor="#111111",
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            text_size=14,
            border_radius=8,
            keyboard_type=ft.KeyboardType.EMAIL
        )
        
        # Campo de contraseña
        self.password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            bgcolor="#111111",
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            text_size=14,
            height=60,
            border_radius=8,
            on_submit=lambda _: self._handle_login()
        )
        
        # Texto de error
        self.error_text = ft.Text(
            "",
            color=COLORS["danger"],
            size=12,
            visible=False,
            text_align=ft.TextAlign.CENTER
        )
        
        # Botón de login
        self.login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar Sesión"),
            height=50,
            bgcolor=COLORS["accent"],
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda _: self._handle_login()
        )
        
        # Logo/Título
        title = ft.Container(
            content=ft.Column([
                ft.Text(
                    "ARK TRIBE MANAGER",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["accent"],
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "FOG TRIBE",
                    size=16,
                    color=COLORS["text_secondary"],
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            margin=ft.margin.only(bottom=40)
        )
        
        # Contenedor del formulario
        form_container = ft.Container(
            content=ft.Column([
                title,
                self.email_field,
                self.password_field,
                self.error_text,
                self.login_button,
                ft.Container(height=10), # Added
                ft.TextButton( # Added
                    content=ft.Text("¿Olvidaste tu contraseña?", size=12, color=COLORS["text_secondary"]), # Added
                    on_click=lambda _: print("Reset pass") # Added
                ) # Added
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20),
            bgcolor=COLORS["card"],
            border_radius=16, # Changed from 12
            padding=40,
            width=400, # Changed from no width
            max_width=400, # Added
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#00000040",
                offset=ft.Offset(0, 4)
            )
        )
        
        # Contenedor principal centrado
        return ft.Container(
            content=ft.Column([
                form_container
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER),
            bgcolor=COLORS["background"],
            expand=True,
            alignment=ft.Alignment(0, 0)
        )
    
    def _handle_login(self):
        """Manejar intento de login"""
        email = self.email_field.value
        password = self.password_field.value
        
        # Validación básica
        if not email or not password:
            self._show_error("Por favor completa todos los campos")
            return
        
        # Deshabilitar botón durante login
        self.login_button.disabled = True
        self.login_button.content.value = "Iniciando sesión..."
        self.login_button.update()
        
        # Llamar callback de login
        self.on_login_success(email, password)
    
    def _show_error(self, message: str):
        """Mostrar mensaje de error"""
        self.error_text.value = message
        self.error_text.visible = True
        self.error_text.update()
        
        # Re-habilitar botón
        if self.login_button:
            self.login_button.disabled = False
            self.login_button.content.value = "Iniciar Sesión"
            self.login_button.update()
    
    def show_error(self, message: str):
        """Método público para mostrar errores"""
        self._show_error(message)
    
    def reset(self):
        """Resetear formulario"""
        if self.login_button:
            self.login_button.disabled = False
            self.login_button.content.value = "Iniciar Sesión"
            self.login_button.update()
