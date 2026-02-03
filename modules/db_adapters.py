# modules/db_adapters.py
"""
Adaptadores específicos que reemplazan las funciones originales
sin romper la compatibilidad del código existente
"""

import sys
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import streamlit as st

# Importar los adaptadores de la base de datos
try:
    from .database import ClientesAdapter, RadarAdapter, Reuniones1to1Adapter
except ImportError:
    # Fallback para importación absoluta
    try:
        from modules.database import ClientesAdapter, RadarAdapter, Reuniones1to1Adapter
    except ImportError:
        # Fallback final - definir adaptadores vacíos
        class ClientesAdapter:
            @staticmethod
            def load_clients():
                return []
            @staticmethod
            def add_client(client_data):
                pass
        
        class RadarAdapter:
            @staticmethod
            def load_config():
                return {}
            @staticmethod
            def save_config(config):
                pass
        
        class Reuniones1to1Adapter:
            @staticmethod
            def load_participantes():
                return pd.DataFrame()
            @staticmethod
            def load_historial():
                return pd.DataFrame()
            @staticmethod
            def save_historial(df):
                pass

# ============================================================================
# ADAPTADOR PARA REPORTE CLIENTES TRIMESTRAL
# ============================================================================

def patch_client_store():
    """Reemplazar funciones de client_store.py con adaptadores de BD"""
    
    # Encontrar el módulo client_store si está cargado
    for module_name, module in sys.modules.items():
        if 'client_store' in module_name and hasattr(module, 'load_clients'):
            # Reemplazar funciones con adaptadores
            module.load_clients = ClientesAdapter.load_clients
            module.add_client = ClientesAdapter.add_client
            break

# ============================================================================
# ADAPTADOR PARA RADAR COMPETIDORES  
# ============================================================================

def patch_radar_config():
    """Reemplazar funciones de config en Radar Competidores"""
    
    # Buscar módulos de radar que tengan load_config y save_config
    for module_name, module in sys.modules.items():
        if ('radar' in module_name.lower() or 'app' in module_name) and hasattr(module, 'load_config'):
            # Reemplazar funciones con adaptadores
            module.load_config = RadarAdapter.load_config
            module.save_config = RadarAdapter.save_config
            break

# ============================================================================
# ADAPTADOR PARA REUNIONES 1TO1
# ============================================================================

def patch_1to1_data_io():
    """Reemplazar funciones de data_io.py con adaptadores de BD"""
    
    # Buscar el módulo data_io en diferentes contextos
    data_io_module = None
    
    # Buscar en sys.modules
    for module_name, module in sys.modules.items():
        if 'data_io' in module_name and hasattr(module, 'load_participantes'):
            data_io_module = module
            break
    
    # Si encontramos el módulo, aplicar parches
    if data_io_module:
        try:
            # Guardar funciones originales como backup
            if not hasattr(data_io_module, '_original_load_participantes'):
                data_io_module._original_load_participantes = data_io_module.load_participantes
                data_io_module._original_load_historial = data_io_module.load_historial
                data_io_module._original_save_historial = data_io_module.save_historial
            
            # Reemplazar con adaptadores
            data_io_module.load_participantes = Reuniones1to1Adapter.load_participantes
            data_io_module.load_historial = Reuniones1to1Adapter.load_historial
            data_io_module.save_historial = Reuniones1to1Adapter.save_historial
            
            # Debug info
            if hasattr(st, 'sidebar') and st.sidebar.checkbox("Debug - Parcheo 1to1", value=False):
                st.sidebar.success(f"✅ Módulo data_io parcheado: {module_name}")
                
        except Exception as e:
            if hasattr(st, 'sidebar'):
                st.sidebar.error(f"Error parcheando data_io: {e}")
    else:
        # Si no encontramos el módulo, intentar parchearlo cuando se importe
        if hasattr(st, 'sidebar') and st.sidebar.checkbox("Debug - Parcheo 1to1", value=False):
            st.sidebar.warning("⚠️ Módulo data_io no encontrado aún")
            st.sidebar.write("Módulos cargados:")
            for name in sys.modules.keys():
                if 'data_io' in name or '1to1' in name:
                    st.sidebar.write(f"- {name}")

# ============================================================================
# FUNCIÓN PRINCIPAL DE PARCHEO
# ============================================================================

def apply_database_patches():
    """Aplicar todos los parches de base de datos"""
    try:
        patch_client_store()
        patch_radar_config() 
        patch_1to1_data_io()
        
        # Debug info para 1to1
        if st.sidebar.checkbox("Debug BD - Reuniones 1to1", value=False):
            status = get_database_status()
            st.sidebar.write("**Estado BD:**")
            st.sidebar.write(f"Conectada: {status['connected']}")
            st.sidebar.write(f"Supabase disponible: {status['supabase_available']}")
            st.sidebar.write(f"URL configurada: {status['url_configured']}")
            st.sidebar.write(f"Key configurada: {status['key_configured']}")
            
            if not status['connected']:
                st.sidebar.info("Usando CSV como fallback")
            
    except Exception as e:
        st.warning(f"Error aplicando parches de BD: {e}")

# ============================================================================
# FUNCIONES DE MIGRACIÓN (OPCIONAL)
# ============================================================================

def migrate_existing_data():
    """Migrar datos existentes a la base de datos (ejecutar una sola vez)"""
    st.info("Función de migración disponible - ejecutar manualmente si es necesario")
    
    # Esta función se puede usar para migrar datos existentes
    # desde archivos locales a la base de datos
    pass