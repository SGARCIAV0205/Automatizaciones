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
from .database import ClientesAdapter, RadarAdapter, Reuniones1to1Adapter

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
    
    # Buscar el módulo data_io
    for module_name, module in sys.modules.items():
        if 'data_io' in module_name and hasattr(module, 'load_participantes'):
            # Reemplazar funciones con adaptadores
            module.load_participantes = Reuniones1to1Adapter.load_participantes
            module.load_historial = Reuniones1to1Adapter.load_historial
            module.save_historial = Reuniones1to1Adapter.save_historial
            break

# ============================================================================
# FUNCIÓN PRINCIPAL DE PARCHEO
# ============================================================================

def apply_database_patches():
    """Aplicar todos los parches de base de datos"""
    try:
        patch_client_store()
        patch_radar_config() 
        patch_1to1_data_io()
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