"""
Módulo de autenticación para el Asistente Virtual AI
"""
import streamlit as st
import hashlib
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def hash_password(password: str) -> str:
    """Crear hash seguro de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verificar contraseña contra hash"""
    return hash_password(password) == hashed

def get_credentials():
    """Obtener credenciales desde variables de entorno o Streamlit secrets"""
    # Intentar primero desde Streamlit secrets (para Streamlit Cloud)
    try:
        username = st.secrets.get("APP_USERNAME", "admin")
        password_hash = st.secrets.get("APP_PASSWORD_HASH")
        
        # Si no hay hash, usar contraseña directa
        if not password_hash:
            default_password = st.secrets.get("APP_PASSWORD", "ubimia2024")
            password_hash = hash_password(default_password)
            
    except (AttributeError, FileNotFoundError):
        # Fallback a variables de entorno (para desarrollo local)
        username = os.getenv("APP_USERNAME", "admin")
        password_hash = os.getenv("APP_PASSWORD_HASH")
        
        # Si no hay hash configurado, usar contraseña por defecto
        if not password_hash:
            default_password = os.getenv("APP_PASSWORD", "ubimia2024")
            password_hash = hash_password(default_password)
    
    return username, password_hash

def check_authentication():
    """Verificar si el usuario está autenticado"""
    return st.session_state.get("authenticated", False)

def login_form():
    """Mostrar formulario de login"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🔐 Acceso al Asistente Virtual AI</h1>
        <p style='color: #666; margin-bottom: 2rem;'>Ingresa tus credenciales para continuar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown("### Iniciar Sesión")
            
            # Formulario de login
            with st.form("login_form"):
                username = st.text_input(
                    "Usuario",
                    placeholder="Ingresa tu usuario",
                    help="Usuario configurado para acceder al sistema"
                )
                
                password = st.text_input(
                    "Contraseña",
                    type="password",
                    placeholder="Ingresa tu contraseña",
                    help="Contraseña configurada para acceder al sistema"
                )
                
                submit_button = st.form_submit_button(
                    "🚀 Ingresar",
                    type="primary",
                    use_container_width=True
                )
                
                if submit_button:
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Acceso autorizado. Redirigiendo...")
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
                        st.info("💡 Verifica tus credenciales e intenta nuevamente")

def authenticate_user(username: str, password: str) -> bool:
    """Autenticar usuario"""
    if not username or not password:
        return False
    
    valid_username, valid_password_hash = get_credentials()
    
    return (username == valid_username and 
            verify_password(password, valid_password_hash))

def logout():
    """Cerrar sesión"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

def render_auth_sidebar():
    """Renderizar información de autenticación en sidebar"""
    if check_authentication():
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Sesión Activa")
            st.success(f"Conectado como: **{st.session_state.get('username', 'Usuario')}**")
            
            if st.button("🚪 Cerrar Sesión", type="secondary"):
                logout()

def require_auth(func):
    """Decorador para requerir autenticación"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            login_form()
            return None
        return func(*args, **kwargs)
    return wrapper

# Función principal de autenticación
def authenticate_app(show_session_info=True):
    """Función principal para manejar autenticación de la app"""
    if not check_authentication():
        login_form()
        st.stop()
    else:
        if show_session_info:
            render_auth_sidebar()