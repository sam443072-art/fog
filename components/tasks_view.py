# components/tasks_view.py
# Vista de gestión de tareas con tags

import flet as ft
from config import COLORS, ROLE_TAGS
from typing import Dict, Any


class TasksView:
    """Vista de tareas de la tribu con tags de roles"""
    
    def __init__(self, firebase_manager):
        self.firebase = firebase_manager
        self.page = None
        
        # Inicializar controles en __init__
        self.task_control = ft.TextField(
            label="Nueva Tarea",
            hint_text="Farmear metal en la montaña norte",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            multiline=True,
            min_lines=1,
            max_lines=3,
            expand=True
        )
        
        self.tag_dropdown = ft.Dropdown(
            label="Tag",
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            options=[
                ft.dropdown.Option("ADMIN", "ADMIN"),
                ft.dropdown.Option("builder", "Builder"),
                ft.dropdown.Option("GH", "Greenhouse"),
                ft.dropdown.Option("BR", "Breeder"),
            ],
            width=200
        )
        
        self.tasks_container = ft.Column([], spacing=10)
        self.error_text = ft.Text("", color=COLORS["danger"], size=12)

    def build(self) -> ft.Container:
        """Construir vista de tareas"""
        
        # Header
        header = ft.Text(
            "Tareas de la Tribu",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=COLORS["text_primary"]
        )
        
        add_button = ft.ElevatedButton(
            content=ft.Text("Añadir Tarea"),
            bgcolor=COLORS["accent"],
            color="#000000",
            height=40,
            on_click=lambda _: self._add_task()
        )
        
        add_form = ft.Container(
            content=ft.Column([
                ft.Row([
                    self.task_control,
                    self.tag_dropdown,
                ], spacing=15, vertical_alignment=ft.CrossAxisAlignment.START, wrap=True),
                self.error_text,
                add_button
            ], spacing=15),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        tasks_list = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Tareas Activas",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["text_secondary"]
                ),
                self.tasks_container
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
                tasks_list
            ], spacing=20),
            padding=30
        )
    
    def _add_task(self):
        """Añadir nueva tarea"""
        self.error_text.value = ""
        
        text = self.task_control.value
        tag = self.tag_dropdown.value
        
        if not text:
            self.error_text.value = "Escribe una descripción."
            if self.page: self.page.update()
            return
        
        if not tag:
            self.error_text.value = "Selecciona un Tag."
            if self.page: self.page.update()
            return
        
        success = self.firebase.add_task(text, tag)
        if success:
            self.task_control.value = ""
            self.tag_dropdown.value = None
            if self.page:
                self.page.update()
            self.refresh_tasks(self.page)
    
    def refresh_tasks(self, page=None):
        """Actualizar lista de tareas"""
        if page:
            self.page = page
        
        tasks = self.firebase.get_tasks()
        self.tasks_container.controls.clear()
        
        if not tasks:
            self.tasks_container.controls.append(
                ft.Text("No hay tareas activas", size=14, color=COLORS["text_secondary"])
            )
        else:
            for task_id, task_data in tasks.items():
                self.tasks_container.controls.append(
                    self._create_task_card(task_id, task_data)
                )
        
        if self.page:
            self.page.update()
    
    def _create_task_card(self, task_id: str, task_data: Dict[str, Any]) -> ft.Container:
        """Crear tarjeta de tarea"""
        text = task_data.get("text", "Sin descripción")
        tag = task_data.get("tag", "ADMIN")
        created_by = task_data.get("created_by", "Unknown")
        
        role_info = ROLE_TAGS.get(tag, {"color": COLORS["text_secondary"], "label": tag})
        
        return ft.Container(
            content=ft.Row([
                ft.Container(width=5, bgcolor=role_info["color"], border_radius=2),
                ft.Column([
                    ft.Text(text, size=14, color=COLORS["text_primary"]),
                    ft.Row([
                        ft.Container(
                            content=ft.Text(role_info["label"], size=9, color="#000000", weight=ft.FontWeight.BOLD),
                            bgcolor=role_info["color"],
                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                            border_radius=4
                        ),
                        ft.Text(f"Por: {created_by}", size=11, color=COLORS["text_secondary"]),
                    ], spacing=10)
                ], spacing=8, expand=True),
                ft.IconButton(
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                    icon_color=COLORS["success"],
                    tooltip="Completar",
                    on_click=lambda _, tid=task_id: self._delete_task(tid)
                )
            ], spacing=15),
            padding=15,
            bgcolor=COLORS["card_hover"],
            border_radius=8,
            border=ft.border.all(1, COLORS["border"])
        )
    
    def _delete_task(self, task_id: str):
        """Eliminar tarea (completar)"""
        self.firebase.delete_task(task_id)
        self.refresh_tasks(self.page)
