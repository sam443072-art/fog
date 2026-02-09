# components/tasks_view.py
# Vista de gestión de tareas con tags

import flet as ft
from config import COLORS, ROLE_TAGS
from typing import Dict, Any


class TasksView:
    """Vista de tareas de la tribu con tags de roles"""
    
    def __init__(self, firebase_manager):
        self.firebase = firebase_manager
        self.tasks_container = None
        self.task_field = None
        self.tag_dropdown = None
        self.page = None
    
    def build(self) -> ft.Container:
        """Construir vista de tareas"""
        
        # Header
        header = ft.Text(
            "Tareas de la Tribu",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=COLORS["text_primary"]
        )
        
        # Formulario para añadir tarea
        self.task_field = ft.TextField(
            label="Nueva Tarea",
            hint_text="Farmear metal en la montaña norte",
            width=400,
            bgcolor=COLORS["card"],
            border_color=COLORS["border"],
            focused_border_color=COLORS["accent"],
            color=COLORS["text_primary"],
            label_style=ft.TextStyle(color=COLORS["text_secondary"]),
            text_size=14,
            multiline=True,
            min_lines=1,
            max_lines=3
        )
        
        self.tag_dropdown = ft.Dropdown(
            label="Tag",
            width=150,
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
            value="ADMIN"
        )
        
        add_button = ft.ElevatedButton(
            content=ft.Text("Añadir Tarea"),
            bgcolor=COLORS["accent"],
            color="#000000",
            height=40,
            on_click=lambda _: self._add_task()
        )
        
        add_form = ft.Container(
            content=ft.Row([
                self.task_field,
                self.tag_dropdown,
                add_button
            ], spacing=15, wrap=True),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=12,
            border=ft.border.all(1, COLORS["border"])
        )
        
        # Contenedor de tareas
        self.tasks_container = ft.Column([], spacing=10)
        
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
        text = self.task_field.value
        tag = self.tag_dropdown.value
        
        if not text or not tag:
            return
        
        success = self.firebase.add_task(text, tag)
        if success:
            self.task_field.value = ""
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
            # Ordenar por timestamp (más reciente primero)
            sorted_tasks = sorted(
                tasks.items(),
                key=lambda x: x[1].get("timestamp", 0),
                reverse=True
            )
            
            for task_id, task_data in sorted_tasks:
                self.tasks_container.controls.append(
                    self._create_task_card(task_id, task_data)
                )
        
        if self.page:
            self.page.update()
    
    def _create_task_card(self, task_id: str, task_data: Dict[str, Any]) -> ft.Container:
        """Crear tarjeta de tarea"""
        text = task_data.get("text", "")
        tag = task_data.get("tag", "ADMIN")
        created_by = task_data.get("created_by", "Unknown")
        
        # Obtener info del tag
        tag_info = ROLE_TAGS.get(tag, {"color": COLORS["text_secondary"], "label": tag})
        
        # Badge del tag
        tag_badge = ft.Container(
            content=ft.Text(
                tag_info["label"],
                size=11,
                color="#000000",
                weight=ft.FontWeight.BOLD
            ),
            bgcolor=tag_info["color"],
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=6
        )
        
        # Botón de eliminar
        delete_button = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_color=COLORS["danger"],
            icon_size=20,
            tooltip="Eliminar tarea",
            on_click=lambda _, tid=task_id: self._delete_task(tid)
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    tag_badge,
                    ft.Container(expand=True),
                    delete_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(text, size=14, color=COLORS["text_primary"]),
                ft.Text(
                    f"Creada por: {created_by}",
                    size=11,
                    color=COLORS["text_secondary"],
                    italic=True
                )
            ], spacing=8),
            padding=15,
            bgcolor=COLORS["card_hover"],
            border_radius=8,
            border=ft.border.all(1, COLORS["border"])
        )
    
    def _delete_task(self, task_id: str):
        """Eliminar tarea"""
        self.firebase.delete_task(task_id)
        self.refresh_tasks(self.page)
