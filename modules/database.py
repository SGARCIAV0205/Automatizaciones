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
            # Fallback: cargar desde CSV original
            try:
                from pathlib import Path
                # Buscar el archivo CSV original
                base_dir = Path(__file__).resolve().parents[1]  # Subir desde modules/ a raíz
                csv_path = base_dir / "1to1" / "data" / "participantes.csv"
                
                if csv_path.exists():
                    df = pd.read_csv(csv_path)
                    if "id_participante" in df.columns and "nombre" in df.columns:
                        return df
                
                # Si no encuentra el CSV, devolver DataFrame con datos de ejemplo
                return pd.DataFrame([
                    {"id_participante": "FER001", "nombre": "Fernando Peiró", "puesto": "Business Operations Director", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""},
                    {"id_participante": "GER001", "nombre": "German Valera", "puesto": "Business Operations Director", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""},
                    {"id_participante": "IVA001", "nombre": "Ivan Castelló", "puesto": "Director de Operación y Proyectos", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""}
                ])
            except Exception as e:
                st.warning(f"Error cargando participantes desde CSV: {e}")
                # Fallback final con datos de ejemplo
                return pd.DataFrame([
                    {"id_participante": "DEMO001", "nombre": "Usuario Demo", "puesto": "Puesto Demo", "area": "Area Demo", "objetivos_anuales": "Objetivos de ejemplo", "fortalezas": "Fortalezas demo", "oportunidades": "Oportunidades demo", "notas_base": ""}
                ])
        
        try:
            response = db.client.table('participantes_1to1').select("*").execute()
            if not response.data:
                # Si BD está conectada pero vacía, cargar desde CSV como migración
                return Reuniones1to1Adapter.load_participantes_fallback()
            
            df = pd.DataFrame(response.data)
            # Renombrar columnas para compatibilidad si es necesario
            if "id" in df.columns and "id_participante" not in df.columns:
                df = df.rename(columns={"id": "id_participante"})
            
            return df
        except Exception as e:
            st.warning(f"Error cargando participantes desde BD: {e}")
            return Reuniones1to1Adapter.load_participantes_fallback()
    
    @staticmethod
    def load_participantes_fallback() -> pd.DataFrame:
        """Fallback para cargar participantes desde CSV"""
        try:
            from pathlib import Path
            base_dir = Path(__file__).resolve().parents[1]
            csv_path = base_dir / "1to1" / "data" / "participantes.csv"
            
            if csv_path.exists():
                return pd.read_csv(csv_path)
        except Exception:
            pass
        
        # Fallback final con datos hardcodeados
        return pd.DataFrame([
            {"id_participante": "FER001", "nombre": "Fernando Peiró", "puesto": "Business Operations Director", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""},
            {"id_participante": "GER001", "nombre": "German Valera", "puesto": "Business Operations Director", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""},
            {"id_participante": "IVA001", "nombre": "Ivan Castelló", "puesto": "Director de Operación y Proyectos", "area": "", "objetivos_anuales": "", "fortalezas": "", "oportunidades": "", "notas_base": ""}
        ])
    
    @staticmethod
    def load_historial() -> pd.DataFrame:
        """Cargar historial (compatible con función original)"""
        if not db.is_connected():
            # Fallback: cargar desde CSV original
            try:
                from pathlib import Path
                base_dir = Path(__file__).resolve().parents[1]
                csv_path = base_dir / "1to1" / "data" / "historial_1to1.csv"
                
                if csv_path.exists():
                    df = pd.read_csv(csv_path, dtype=str)
                    # Asegurar columnas requeridas
                    required_columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                                      "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                                      "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                    for col in required_columns:
                        if col not in df.columns:
                            df[col] = None
                    return df[required_columns]
                
                # Si no existe el archivo, crear DataFrame vacío con columnas correctas
                columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                          "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                          "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                return pd.DataFrame(columns=columns)
            except Exception as e:
                st.warning(f"Error cargando historial desde CSV: {e}")
                columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                          "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                          "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                return pd.DataFrame(columns=columns)
        
        try:
            response = db.client.table('historial_1to1').select("*").order("fecha_reunion", desc=True).execute()
            if not response.data:
                columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                          "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                          "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                return pd.DataFrame(columns=columns)
            
            return pd.DataFrame(response.data)
        except Exception as e:
            st.warning(f"Error cargando historial desde BD: {e}")
            return Reuniones1to1Adapter.load_historial_fallback()
    
    @staticmethod
    def load_historial_fallback() -> pd.DataFrame:
        """Fallback para cargar historial desde CSV"""
        try:
            from pathlib import Path
            base_dir = Path(__file__).resolve().parents[1]
            csv_path = base_dir / "1to1" / "data" / "historial_1to1.csv"
            
            if csv_path.exists():
                df = pd.read_csv(csv_path, dtype=str)
                required_columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                                  "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                                  "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = None
                return df[required_columns]
        except Exception:
            pass
        
        # Fallback final - DataFrame vacío
        columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                  "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                  "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
        return pd.DataFrame(columns=columns)
    
    @staticmethod
    def save_historial(historial_df: pd.DataFrame):
        """Guardar historial (compatible con función original)"""
        if not db.is_connected():
            # Fallback: guardar en CSV original
            try:
                from pathlib import Path
                base_dir = Path(__file__).resolve().parents[1]
                data_dir = base_dir / "1to1" / "data"
                data_dir.mkdir(parents=True, exist_ok=True)
                csv_path = data_dir / "historial_1to1.csv"
                
                # Asegurar columnas correctas
                required_columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                                  "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                                  "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
                
                # Filtrar solo las columnas que existen
                existing_columns = [col for col in required_columns if col in historial_df.columns]
                df_to_save = historial_df[existing_columns]
                
                df_to_save.to_csv(csv_path, index=False)
                return
            except Exception as e:
                st.warning(f"Error guardando historial en CSV: {e}")
                return
        
        try:
            # Convertir DataFrame a lista de diccionarios
            records = historial_df.to_dict('records')
            
            # Insertar nuevos registros (el último registro es el nuevo)
            if records:
                last_record = records[-1]
                db.client.table('historial_1to1').insert(last_record).execute()
        except Exception as e:
            st.warning(f"Error guardando historial en BD: {e}")
            # Fallback a CSV si falla la BD
            Reuniones1to1Adapter.save_historial_fallback(historial_df)
    
    @staticmethod
    def save_historial_fallback(historial_df: pd.DataFrame):
        """Fallback para guardar historial en CSV"""
        try:
            from pathlib import Path
            base_dir = Path(__file__).resolve().parents[1]
            data_dir = base_dir / "1to1" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            csv_path = data_dir / "historial_1to1.csv"
            
            required_columns = ["id_participante", "fecha_reunion", "health_energia", "health_carga_trabajo", 
                              "health_alineacion_objetivos", "health_notas", "preguntas_generadas",
                              "insight_coaching", "notas_reunion", "compromisos", "fecha_proxima_reunion"]
            
            existing_columns = [col for col in required_columns if col in historial_df.columns]
            df_to_save = historial_df[existing_columns]
            
            df_to_save.to_csv(csv_path, index=False)
        except Exception as e:
            st.error(f"Error en fallback de guardado: {e}")

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