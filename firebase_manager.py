# firebase_manager.py
# Gestión de conexión y operaciones con Firebase

import pyrebase
import time
from typing import Optional, Dict, Any
from config import FIREBASE_CONFIG, ADMIN_TIMEOUT


class FirebaseManager:
    """Gestor centralizado para todas las operaciones de Firebase"""
    
    def __init__(self):
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.user = None
        self.id_token = None
        self.user_email = None
        
    def login(self, email: str, password: str) -> tuple[bool, str]:
        """
        Autenticar usuario con Firebase
        Returns: (success: bool, message: str)
        """
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
            self.id_token = self.user['idToken']
            self.user_email = email.split('@')[0]  # Username sin dominio
            return True, "Login exitoso"
        except Exception as e:
            error_msg = str(e)
            if "INVALID_PASSWORD" in error_msg:
                return False, "Contraseña incorrecta"
            elif "EMAIL_NOT_FOUND" in error_msg:
                return False, "Email no registrado"
            elif "INVALID_EMAIL" in error_msg:
                return False, "Email inválido"
            else:
                return False, f"Error de autenticación: {error_msg}"
    
    def logout(self):
        """Cerrar sesión y limpiar heartbeat"""
        if self.user_email:
            try:
                self.db.child("admin_status").child(self.user_email).update({
                    "active": False,
                    "last_heartbeat": int(time.time())
                }, self.id_token)
            except:
                pass
        self.user = None
        self.id_token = None
        self.user_email = None
    
    def is_authenticated(self) -> bool:
        """Verificar si hay sesión activa"""
        return self.user is not None and self.id_token is not None
    
    # ==================== GENERADORES ====================
    
    def add_generator(self, name: str, duration_days: int) -> bool:
        """Añadir nuevo generador"""
        try:
            generator_data = {
                "name": name,
                "start_timestamp": int(time.time()),
                "duration_seconds": duration_days * 24 * 60 * 60,
                "created_by": self.user_email
            }
            self.db.child("generators").push(generator_data, self.id_token)
            return True
        except Exception as e:
            print(f"Error añadiendo generador: {e}")
            return False
    
    def get_generators(self) -> Dict[str, Any]:
        """Obtener todos los generadores"""
        try:
            data = self.db.child("generators").get(self.id_token)
            return data.val() if data.val() else {}
        except:
            return {}
    
    def delete_generator(self, generator_id: str) -> bool:
        """Eliminar generador"""
        try:
            self.db.child("generators").child(generator_id).remove(self.id_token)
            return True
        except:
            return False
    
    # ==================== TAREAS ====================
    
    def add_task(self, text: str, tag: str) -> bool:
        """Añadir nueva tarea"""
        try:
            task_data = {
                "text": text,
                "tag": tag,
                "created_by": self.user_email,
                "timestamp": int(time.time())
            }
            self.db.child("tasks").push(task_data, self.id_token)
            return True
        except Exception as e:
            print(f"Error añadiendo tarea: {e}")
            return False
    
    def get_tasks(self) -> Dict[str, Any]:
        """Obtener todas las tareas"""
        try:
            data = self.db.child("tasks").get(self.id_token)
            return data.val() if data.val() else {}
        except:
            return {}
    
    def delete_task(self, task_id: str) -> bool:
        """Eliminar tarea"""
        try:
            self.db.child("tasks").child(task_id).remove(self.id_token)
            return True
        except:
            return False
    
    # ==================== MIEMBROS ====================
    
    def add_member(self, name: str, discord: str, vouch: str, trust: str, roles: list) -> bool:
        """Añadir nuevo miembro"""
        try:
            member_data = {
                "name": name,
                "discord": discord,
                "vouch": vouch,
                "trust": trust,
                "roles": roles
            }
            self.db.child("members").push(member_data, self.id_token)
            return True
        except Exception as e:
            print(f"Error añadiendo miembro: {e}")
            return False
    
    def get_members(self) -> Dict[str, Any]:
        """Obtener todos los miembros"""
        try:
            data = self.db.child("members").get(self.id_token)
            return data.val() if data.val() else {}
        except:
            return {}
    
    def delete_member(self, member_id: str) -> bool:
        """Eliminar miembro"""
        try:
            self.db.child("members").child(member_id).remove(self.id_token)
            return True
        except:
            return False
    
    def update_member(self, member_id: str, data: Dict[str, Any]) -> bool:
        """Actualizar datos de miembro"""
        try:
            self.db.child("members").child(member_id).update(data, self.id_token)
            return True
        except:
            return False
    
    # ==================== ADMIN STATUS (HEARTBEAT) ====================
    
    def update_heartbeat(self, roles: list) -> bool:
        """Actualizar heartbeat del admin actual"""
        try:
            status_data = {
                "username": self.user_email,
                "last_heartbeat": int(time.time()),
                "active": True,
                "roles": roles
            }
            self.db.child("admin_status").child(self.user_email).set(status_data, self.id_token)
            return True
        except Exception as e:
            print(f"Error actualizando heartbeat: {e}")
            return False
    
    def get_active_admins(self) -> Dict[str, Any]:
        """Obtener admins activos (últimos 2 minutos)"""
        try:
            data = self.db.child("admin_status").get(self.id_token)
            if not data.val():
                return {}
            
            current_time = int(time.time())
            active_admins = {}
            
            for admin_id, admin_data in data.val().items():
                last_beat = admin_data.get("last_heartbeat", 0)
                if current_time - last_beat < ADMIN_TIMEOUT:
                    active_admins[admin_id] = admin_data
                    active_admins[admin_id]["active"] = True
                else:
                    # Marcar como inactivo si pasó el timeout
                    active_admins[admin_id] = admin_data
                    active_admins[admin_id]["active"] = False
            
            return active_admins
        except:
            return {}
