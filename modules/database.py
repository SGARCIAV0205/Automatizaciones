# modules/database.py
"""
Módulo de base de datos usando Supabase (PostgreSQL gratuito)
Mantiene compatibilidad total con el código existente
"""

import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("Supabase no está instalado. Usando almacenamiento local temporal.")

class DatabaseManager:
    def __init__(self):
        self.client: Optional[Client] = None
        self.connected = False
        self._init_connection()
    
    def _init_connection(self):
        """Inicializar conexión con Supabase"""
        if not SUPABASE_AVAILABLE:
            return
        
        try:
            # Obtener credenciales desde Streamlit secrets o variables de entorno
            url = self._get_config("SUPABASE_URL")
            key = self._get_config("SUPABASE_ANON_KEY")
            
            if url and key:
                self.client = create_client(url, key)
                self.connected = True
                self._ensure_tables_exist()
            else:
                st.info("Configuración de Supabase no encontrada. Usando almacenamiento local.")
        except Exception as e:
            st.warning(f"Error conectando a Supabase: {e}. Usando almacenamiento local.")
    
    def _get_config(self, key: str) -> Optional[str]:
        """Obtener configuración desde secrets o env"""
        try:
            return st.secrets.get(key)
        except (AttributeError, FileNotFoundError):
            return os.getenv(key)
    
    def _ensure_tables_exist(self):
        """Crear tablas si no existen"""
        if not self.connected:
            return
        
        try:
            # Las tablas se crean desde el dashboard de Supabase
            # Aquí solo verificamos que existan
            tables = ['clientes', 'competidores', 'configuracion_radar', 'participantes_1to1', 'historial_1to1']
            for table in tables:
                try:
                    self.client.table(table).select("*").limit(1).execute()
                except Exception:
                    st.warning(f"Tabla '{table}' no existe en Supabase. Créala desde el dashboard.")
        except Exception as e:
            st.warning(f"Error verificando tablas: {e}")
    
    def is_connected(self) -> bool:
        """Verificar si está conectado a la base de datos"""
        return self.connected and self.client is not None

# Instancia global
db = DatabaseManager()

# ============================================================================
# ADAPTADORES PARA CADA MÓDULO (mantienen compatibilidad total)
# ============================================================================

class ClientesAdapter:
    """Adaptador para Reporte Clientes Trimestral - mantiene compatibilidad con client_store.py"""
    
    @staticmethod
    def load_clients() -> List[Dict]:
        """Cargar clientes (compatible con función original)"""
        if not db.is_connected():
            return []  # Fallback a lista vacía si no hay BD
        
        try:
            response = db.client.table('clientes').select("*").execute()
            clients = []
            for row in response.data:
                clients.append({
                    "name": row["nombre"],
                    "sector": row.get("sector", ""),
                    "keywords": json.loads(row.get("keywords", "[]"))
                })
            return clients
        except Exception as e:
            st.error(f"Error cargando clientes: {e}")
            return []
    
    @staticmethod
    def add_client(client_data: Dict, persist: bool = True) -> List[Dict]:
        """Agregar cliente (compatible con función original)"""
        if not persist or not db.is_connected():
            # Fallback: devolver lista con el cliente actual
            return [client_data]
        
        try:
            # Verificar si ya existe
            existing = db.client.table('clientes').select("*").eq("nombre", client_data["name"]).execute()
            if existing.data:
                return ClientesAdapter.load_clients()  # Ya existe
            
            # Insertar nuevo cliente
            db.client.table('clientes').insert({
                "nombre": client_data["name"],
                "sector": client_data.get("sector", ""),
                "keywords": json.dumps(client_data.get("keywords", [])),
                "fecha_creacion": datetime.now().isoformat()
            }).execute()
            
            return ClientesAdapter.load_clients()
        except Exception as e:
            st.error(f"Error agregando cliente: {e}")
            return [client_data]

class RadarAdapter:
    """Adaptador para Radar Competidores - mantiene compatibilidad con config.yaml"""
    
    @staticmethod
    def load_config() -> Dict:
        """Cargar configuración (compatible con función original)"""
        if not db.is_connected():
            # Fallback a configuración por defecto
            return {
                "periodo": "2025-01",
                "use_llm": False,
                "openai_model": "gpt-4o-mini",
                "notas_globales": "",
                "competitors": [],
                "competitor_notes": {}
            }
        
        try:
            # Cargar configuración general
            config_response = db.client.table('configuracion_radar').select("*").execute()
            config = {}
            for row in config_response.data:
                if row["clave"] in ["competitors", "competitor_notes"]:
                    config[row["clave"]] = json.loads(row["valor"])
                elif row["clave"] == "use_llm":
                    config[row["clave"]] = row["valor"].lower() == "true"
                else:
                    config[row["clave"]] = row["valor"]
            
            # Cargar competidores
            comp_response = db.client.table('competidores').select("*").eq("activo", True).execute()
            competitors = [row["nombre"] for row in comp_response.data]
            competitor_notes = {row["nombre"]: row["notas"] for row in comp_response.data if row["notas"]}
            
            config["competitors"] = competitors
            config["competitor_notes"] = competitor_notes
            
            return config
        except Exception as e:
            st.error(f"Error cargando configuración: {e}")
            return {"periodo": "2025-01", "competitors": [], "competitor_notes": {}}
    
    @staticmethod
    def save_config(cfg: Dict):
        """Guardar configuración (compatible con función original)"""
        if not db.is_connected():
            return
        
        try:
            # Guardar configuración general
            for key, value in cfg.items():
                if key in ["competitors", "competitor_notes"]:
                    continue  # Se manejan por separado
                
                # Upsert configuración
                db.client.table('configuracion_radar').upsert({
                    "clave": key,
                    "valor": str(value)
                }).execute()
            
            # Actualizar competidores
            if "competitors" in cfg:
                # Desactivar todos primero
                db.client.table('competidores').update({"activo": False}).neq("id", 0).execute()
                
                # Insertar/activar competidores actuales
                for comp in cfg["competitors"]:
                    notas = cfg.get("competitor_notes", {}).get(comp, "")
                    db.client.table('competidores').upsert({
                        "nombre": comp,
                        "notas": notas,
                        "activo": True
                    }).execute()
        except Exception as e:
            st.error(f"Error guardando configuración: {e}")

class Reuniones1to1Adapter:
    """Adaptador para Reuniones 1to1 - mantiene compatibilidad con data_io.py"""
    
    @staticmethod
    def load_participantes() -> pd.DataFrame:
        """Cargar participantes (compatible con función original)"""
        if not db.is_connected():
            # Fallback a DataFrame vacío con columnas correctas
            return pd.DataFrame(columns=["id_participante", "nombre", "email", "objetivos_anuales", "fortalezas", "oportunidades_mejora"])
        
        try:
            response = db.client.table('participantes_1to1').select("*").execute()
            if not response.data:
                return pd.DataFrame(columns=["id_participante", "nombre", "email", "objetivos_anuales", "fortalezas", "oportunidades_mejora"])
            
            df = pd.DataFrame(response.data)
            # Renombrar columnas para compatibilidad
            if "id" in df.columns:
                df = df.rename(columns={"id": "id_participante"})
            
            return df
        except Exception as e:
            st.error(f"Error cargando participantes: {e}")
            return pd.DataFrame(columns=["id_participante", "nombre", "email"])
    
    @staticmethod
    def load_historial() -> pd.DataFrame:
        """Cargar historial (compatible con función original)"""
        if not db.is_connected():
            # Fallback a DataFrame vacío
            columns = ["id_participante", "fecha_reunion", "objetivos_reunion", "puntos_discutidos", 
                      "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
            return pd.DataFrame(columns=columns)
        
        try:
            response = db.client.table('historial_1to1').select("*").order("fecha_reunion", desc=True).execute()
            if not response.data:
                columns = ["id_participante", "fecha_reunion", "objetivos_reunion", "puntos_discutidos", 
                          "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                return pd.DataFrame(columns=columns)
            
            return pd.DataFrame(response.data)
        except Exception as e:
            st.error(f"Error cargando historial: {e}")
            return pd.DataFrame()
    
    @staticmethod
    def save_historial(historial_df: pd.DataFrame):
        """Guardar historial (compatible con función original)"""
        if not db.is_connected():
            return
        
        try:
            # Convertir DataFrame a lista de diccionarios
            records = historial_df.to_dict('records')
            
            # Insertar nuevos registros (el último registro es el nuevo)
            if records:
                last_record = records[-1]
                db.client.table('historial_1to1').insert(last_record).execute()
        except Exception as e:
            st.error(f"Error guardando historial: {e}")

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def get_database_status() -> Dict[str, Any]:
    """Obtener estado de la base de datos para debugging"""
    return {
        "connected": db.is_connected(),
        "supabase_available": SUPABASE_AVAILABLE,
        "url_configured": bool(db._get_config("SUPABASE_URL")),
        "key_configured": bool(db._get_config("SUPABASE_ANON_KEY"))
    }

def render_database_status_sidebar():
    """Mostrar estado de BD en sidebar (opcional)"""
    if st.sidebar.checkbox("Mostrar estado BD", value=False):
        status = get_database_status()
        if status["connected"]:
            st.sidebar.success("✅ Base de datos conectada")
        else:
            st.sidebar.warning("⚠️ Usando almacenamiento local")