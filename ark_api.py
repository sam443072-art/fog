# ark_api.py
# Cliente para la API de ARK Status

import requests
from typing import Optional, Dict, Any
from config import ARKSTATUS_API_KEY, ARKSTATUS_URL, ARK_SERVER_ID


class ARKStatusAPI:
    """Cliente para consultar el estado del servidor ARK"""
    
    def __init__(self):
        self.api_key = ARKSTATUS_API_KEY
        self.base_url = ARKSTATUS_URL
        self.server_id = ARK_SERVER_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_server_status(self) -> Optional[Dict[str, Any]]:
        """
        Obtener estado actual del servidor
        Returns: Dict con información del servidor o None si hay error
        """
        try:
            url = f"{self.base_url}/{self.server_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_server_data(data)
            else:
                print(f"Error API: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("Timeout al consultar API")
            return None
        except Exception as e:
            print(f"Error consultando servidor: {e}")
            return None
    
    def _parse_server_data(self, raw_data: Dict) -> Dict[str, Any]:
        """Parsear y estructurar datos de la API"""
        try:
            server_data = raw_data.get("data", {})
            
            return {
                "name": server_data.get("name", "Unknown Server"),
                "map": server_data.get("map", "Unknown Map"),
                "players": server_data.get("players", 0),
                "max_players": server_data.get("maxPlayers", 70),
                "ping": server_data.get("ping", 0),
                "version": server_data.get("version", "N/A"),
                "online": server_data.get("online", False),
                "uptime": server_data.get("uptime", 0),
                "peak_players": server_data.get("peakPlayers", 0),
                "platform": server_data.get("platform", "PC"),
                "last_update": server_data.get("lastUpdate", "N/A")
            }
        except Exception as e:
            print(f"Error parseando datos: {e}")
            return {
                "name": "Error",
                "map": "N/A",
                "players": 0,
                "max_players": 70,
                "ping": 0,
                "version": "N/A",
                "online": False,
                "uptime": 0,
                "peak_players": 0,
                "platform": "N/A",
                "last_update": "N/A"
            }
