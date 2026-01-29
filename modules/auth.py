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
    """Mostrar formulario de login personalizado"""
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <div class="ub-badge" style="margin-bottom: 1.5rem;">ASISTENTE VIRTUAL AI</div>
        <h1 style='color: var(--ub-white); font-weight: 700; margin-bottom: 0.5rem;'>Acceso Autorizado</h1>
        <p style='color: var(--ub-gray); margin-bottom: 2rem; font-size: 16px;'>Ingresa tus credenciales para continuar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Crear una tarjeta personalizada para el login
        st.markdown("""
        <div class="ub-card" style="margin-bottom: 2rem;">
        """, unsafe_allow_html=True)
        
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
                "Ingresar",
                type="primary",
                use_container_width=True
            )
            
            if submit_button:
                if authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Acceso autorizado. Redirigiendo...")
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
                    st.info("Verifica tus credenciales e intenta nuevamente")
        
        st.markdown("</div>", unsafe_allow_html=True)

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
    """Renderizar información de autenticación en sidebar al final"""
    if check_authentication():
        with st.sidebar:
            # CSS para posicionar la información de sesión al final del sidebar
            st.markdown("""
            <style>
            /* Contenedor para la información de sesión al final */
            .session-info-bottom {
                position: fixed;
                bottom: 20px;
                left: 20px;
                right: 20px;
                width: calc(100% - 40px);
                max-width: 280px;
                z-index: 999;
            }
            
            /* Ajustar para el ancho del sidebar */
            @media (min-width: 768px) {
                .session-info-bottom {
                    left: 20px;
                    width: calc(21rem - 40px);
                }
            }
            </style>
            
            <div class="session-info-bottom">
                <div style="
                    background: var(--ub-navy-2);
                    border: 1px solid rgba(46,230,166,0.3);
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    margin-bottom: 1rem;
                ">
                    <div style="
                        color: var(--ub-mint);
                        font-size: 14px;
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                    ">SESIÓN ACTIVA</div>
                    <div style="
                        color: var(--ub-white);
                        font-size: 16px;
                        font-weight: 700;
                        margin-bottom: 1rem;
                    ">""" + st.session_state.get('username', 'Usuario') + """</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Crear un contenedor invisible para el botón que también esté al final
            st.markdown("""
            <div style="position: fixed; bottom: 80px; left: 20px; width: calc(21rem - 40px); z-index: 999;">
            """, unsafe_allow_html=True)
            
            # Botón de cerrar sesión
            if st.button("Cerrar Sesión", type="secondary", use_container_width=True, key="logout_bottom"):
                logout()
                
            st.markdown("</div>", unsafe_allow_html=True)

def require_auth(func):
    """Decorador para requerir autenticación"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            login_form()
            return None
        return func(*args, **kwargs)
    return wrapper

# Función principal de autenticación
def authenticate_app():
    """Función principal para manejar autenticación de la app"""
    if not check_authentication():
        login_form()
        st.stop()
    else:
        render_auth_sidebar()

def render_session_footer():
    """Renderizar información de sesión al final de cada módulo"""
    if check_authentication():
        st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="
                background: var(--ub-navy-2);
                border: 1px solid rgba(46,230,166,0.2);
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                margin: 1rem 0;
            ">
                <div style="
                    color: var(--ub-mint);
                    font-size: 12px;
                    font-weight: 800;
                    letter-spacing: 1px;
                    margin-bottom: 0.5rem;
                ">SESIÓN ACTIVA</div>
                <div style="
                    color: var(--ub-white);
                    font-size: 18px;
                    font-weight: 700;
                    margin-bottom: 1rem;
                ">Conectado como: """ + st.session_state.get('username', 'Usuario') + """</div>
                <div style="
                    color: var(--ub-gray);
                    font-size: 14px;
                ">Asistente Virtual AI - Ubimia</div>
            </div>
            """, unsafe_allow_html=True)