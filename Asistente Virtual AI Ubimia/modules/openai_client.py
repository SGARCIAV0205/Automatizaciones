"""
Módulo para manejar la conexión con OpenAI API
"""
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración específica por módulo
MODEL_CONFIG = {
    "minutas": {
        "model": "gpt-4o-mini",
        "temperature": 0.25,
        "max_tokens": 2000
    },
    "1to1": {
        "model": "gpt-4o-mini", 
        "temperature": 0.4,
        "max_tokens": 1000
    },
    "competidores": {
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "max_tokens": 1500
    },
    "clientes": {
        "model": "gpt-4o-mini",
        "temperature": 0.35,
        "max_tokens": 1800
    },
    "default": {
        "model": _get_config_value("DEFAULT_MODEL", "gpt-4o-mini"),
        "temperature": float(_get_config_value("DEFAULT_TEMPERATURE", "0.3")),
        "max_tokens": int(_get_config_value("DEFAULT_MAX_TOKENS", "1500"))
    }
}

def _get_config_value(key: str, default: str) -> str:
    """Obtener valor de configuración desde Streamlit secrets o variables de entorno"""
    try:
        # Intentar primero desde Streamlit secrets
        return st.secrets.get(key, default)
    except (AttributeError, FileNotFoundError):
        # Fallback a variables de entorno
        return os.getenv(key, default)

class OpenAIClient:
    def __init__(self):
        self.api_key = None
        self.client = None
    
    def initialize_client(self, api_key: str = None):
        """Inicializar el cliente de OpenAI"""
        if api_key:
            self.api_key = api_key
        else:
            # Intentar obtener desde Streamlit secrets primero
            try:
                self.api_key = st.secrets.get("OPENAI_API_KEY")
            except (AttributeError, FileNotFoundError):
                # Fallback a variables de entorno
                self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            return False, "No se encontró la API key de OpenAI"
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            # Probar la conexión
            self.client.models.list()
            return True, "Conexión exitosa con OpenAI"
        except Exception as e:
            return False, f"Error al conectar con OpenAI: {str(e)}"
    
    def chat_completion(self, messages: list, system_prompt: str = None, module: str = "default"):
        """Generar respuesta usando ChatGPT con configuración específica por módulo"""
        if not self.client:
            return None, "Cliente de OpenAI no inicializado"
        
        try:
            # Obtener configuración del módulo
            config = MODEL_CONFIG.get(module, MODEL_CONFIG["default"])
            
            # Preparar mensajes
            formatted_messages = []
            
            if system_prompt:
                formatted_messages.append({
                    "role": "system", 
                    "content": system_prompt
                })
            
            formatted_messages.extend(messages)
            
            # Hacer la llamada a la API con configuración específica
            response = self.client.chat.completions.create(
                model=config["model"],
                messages=formatted_messages,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"]
            )
            
            return response.choices[0].message.content, None
            
        except Exception as e:
            return None, f"Error en la API de OpenAI: {str(e)}"
    
    def is_connected(self):
        """Verificar si el cliente está conectado"""
        return self.client is not None
    
    # Funciones específicas para cada módulo
    def enhance_minutes(self, raw_text: str, context: str = ""):
        """Mejorar minutas usando AI"""
        system_prompt = """Eres un asistente especializado en generar minutas de reuniones profesionales. 
        Tu tarea es tomar texto crudo de una transcripción y convertirlo en una minuta estructurada y clara.
        
        Debes extraer y estructurar:
        1. **Objetivos principales** de la reunión
        2. **Resumen ejecutivo** de los puntos discutidos
        3. **Acuerdos y decisiones** tomadas
        4. **Tareas asignadas** con responsables y fechas (si se mencionan)
        
        Formato de respuesta:
        ## Objetivos
        [Lista de objetivos identificados]
        
        ## Resumen Ejecutivo
        [Resumen conciso de la discusión]
        
        ## Acuerdos y Decisiones
        [Decisiones tomadas durante la reunión]
        
        ## Tareas Asignadas
        - [Tarea] - Responsable: [Nombre] - Fecha: [Si se menciona]
        
        Mantén un tono profesional, conciso y objetivo."""
        
        user_message = f"""
        Contexto adicional: {context}
        
        Transcripción de la reunión:
        {raw_text}
        
        Por favor, genera una minuta estructurada basada en esta transcripción.
        """
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat_completion(messages, system_prompt, "minutas")
    
    def analyze_competitors(self, competitor_data: str, analysis_type: str = "general"):
        """Analizar información de competidores"""
        system_prompt = f"""Eres un analista de mercado especializado en análisis competitivo.
        Tu tarea es analizar información sobre competidores y generar insights valiosos.
        
        Tipo de análisis solicitado: {analysis_type}
        
        Estructura tu análisis en:
        ## Resumen Ejecutivo
        [Puntos clave del análisis]
        
        ## Fortalezas Identificadas
        [Fortalezas de los competidores]
        
        ## Debilidades y Oportunidades
        [Áreas de mejora y oportunidades para nosotros]
        
        ## Recomendaciones Estratégicas
        [Acciones recomendadas basadas en el análisis]
        
        Proporciona un análisis estructurado, objetivo y basado en datos."""
        
        messages = [{"role": "user", "content": competitor_data}]
        return self.chat_completion(messages, system_prompt, "competidores")
    
    def generate_client_insights(self, client_data: str, period: str = "trimestral"):
        """Generar insights para reportes de clientes"""
        system_prompt = f"""Eres un consultor de negocios especializado en análisis de clientes.
        Tu tarea es analizar datos de clientes y generar insights para reportes {period}.
        
        Estructura tu análisis en:
        ## Análisis de Tendencias
        [Patrones y tendencias identificadas]
        
        ## Oportunidades de Crecimiento
        [Áreas de expansión y mejora]
        
        ## Evaluación de Riesgos
        [Riesgos potenciales identificados]
        
        ## Recomendaciones Estratégicas
        [Acciones específicas recomendadas]
        
        ## Próximos Pasos
        [Plan de acción sugerido]
        
        Mantén un enfoque profesional, orientado a resultados y basado en datos."""
        
        messages = [{"role": "user", "content": client_data}]
        return self.chat_completion(messages, system_prompt, "clientes")
    
    def improve_1to1_preparation(self, employee_data: str, previous_notes: str = ""):
        """Mejorar preparación de reuniones 1:1"""
        system_prompt = """Eres un coach de liderazgo especializado en reuniones 1:1 efectivas.
        Tu tarea es ayudar a preparar reuniones productivas y significativas.
        
        Estructura tu respuesta en:
        ## Temas Prioritarios a Discutir
        [Temas más importantes basados en la información]
        
        ## Preguntas de Seguimiento Sugeridas
        [Preguntas específicas para profundizar]
        
        ## Objetivos de Desarrollo
        [Áreas de crecimiento identificadas]
        
        ## Acciones de Apoyo
        [Formas específicas de brindar apoyo]
        
        ## Preparación para la Próxima Reunión
        [Elementos a considerar para el futuro]
        
        Mantén un enfoque empático, constructivo y orientado al crecimiento profesional."""
        
        user_message = f"""
        Información del empleado: {employee_data}
        Notas de reuniones previas: {previous_notes}
        
        Ayúdame a preparar una reunión 1:1 efectiva y productiva.
        """
        
        messages = [{"role": "user", "content": user_message}]
        return self.chat_completion(messages, system_prompt, "1to1")

# Instancia global del cliente
openai_client = OpenAIClient()

# Funciones de utilidad para la UI
def render_openai_config_sidebar():
    """Renderizar configuración de OpenAI en sidebar"""
    with st.sidebar:
        st.header("🤖 Configuración AI")
        
        # Verificar si ya está conectado
        if hasattr(st.session_state, 'openai_connected') and st.session_state.openai_connected:
            st.success("✅ OpenAI conectado")
            st.caption("Usando gpt-4o-mini con configuración optimizada por módulo")
            if st.button("🔄 Reconectar"):
                del st.session_state.openai_connected
                st.rerun()
            return True
        
        # Input para API Key
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Ingresa tu API key de OpenAI para habilitar funciones de AI",
            placeholder="sk-..."
        )
        
        if st.button("🔗 Conectar AI"):
            if api_key_input:
                success, message = openai_client.initialize_client(api_key_input)
                if success:
                    st.success(message)
                    st.session_state.openai_connected = True
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Por favor ingresa tu API key")
        
        st.info("💡 Las funciones de AI son opcionales. Puedes usar la aplicación sin ellas.")
        return False

def is_openai_available():
    """Verificar si OpenAI está disponible"""
    return (hasattr(st.session_state, 'openai_connected') and 
            st.session_state.openai_connected and 
            openai_client.is_connected())

def get_model_info(module: str = "default"):
    """Obtener información del modelo para un módulo específico"""
    config = MODEL_CONFIG.get(module, MODEL_CONFIG["default"])
    return f"Modelo: {config['model']} | Temp: {config['temperature']} | Tokens: {config['max_tokens']}"