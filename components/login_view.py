# components/login_view.py
# Vista de inicio de sesión de la aplicación

import flet as ft
from config import COLORS


class LoginView:
    """Vista de login para autenticar usuarios con Firebase"""
    
    def __init__(self, firebase_manager, on_login_success):
        self.firebase = firebase_manager
        self.on_login_success = on_login_success
        self.page = None
        
        # Inicializar todos los controles en __init__
        self.email_field = ft.TextField(
            label="Email",
            bgcolor="#111111",
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            text_size=14,
            border_radius=8,
            keyboard_type=ft.KeyboardType.EMAIL,
            on_submit=lambda _: self.password_field.focus()
        )
        
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
        
        self.error_text = ft.Text(
            "",
            color=COLORS["danger"],
            size=12,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.login_button = ft.ElevatedButton(
            content=ft.Text("Iniciar Sesión", size=16, weight=ft.FontWeight.BOLD),
            height=50,
            bgcolor=COLORS["accent"],
            color="#000000",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=lambda _: self._handle_login()
        )
        
        self.loading_indicator = ft.ProgressRing(
            visible=False, 
            width=24, 
            height=24, 
            color=COLORS["accent"]
        )

    def build(self) -> ft.Container:
        """Construir la interfaz de login"""
        
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
                ft.Row([self.login_button, self.loading_indicator], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(height=10),
                ft.TextButton(
                    content=ft.Text("¿Olvidaste tu contraseña?", size=12, color=COLORS["text_secondary"]),
                    on_click=lambda _: self._show_demo_info()
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=40,
            bgcolor=COLORS["card"],
            border_radius=16,
            width=400,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color="#00000040",
                offset=ft.Offset(0, 4)
            )
        )
        
        # Contenedor principal para centrar
        return ft.Container(
            content=ft.Column([
                form_container
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            bgcolor=COLORS["background"]
        )
    
    def _handle_login(self):
        """Procesar el intento de inicio de sesión"""
        email = self.email_field.value
        password = self.password_field.value
        
        if not email or not password:
            self.error_text.value = "Por favor ingresa email y contraseña."
            self.error_text.update()
            return
            
        # Mostrar loading
        self.login_button.disabled = True
        self.loading_indicator.visible = True
        self.error_text.value = ""
        self.email_field.update()
        self.password_field.update()
        if self.page: self.page.update()
        
        # Intentar login
        user = self.firebase.login(email, password)
        
        if user:
            self.on_login_success(email)
        else:
            self.error_text.value = "Credenciales incorrectas o error de conexión."
            self.login_button.disabled = False
            self.loading_indicator.visible = False
            if self.page: self.page.update()

    def _show_demo_info(self):
        """Mostrar información de ayuda"""
        self.error_text.value = "Contacta al administrador para recuperar tu cuenta."
        if self.page: self.page.update()
