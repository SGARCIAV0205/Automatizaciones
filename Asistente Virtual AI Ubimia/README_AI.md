# 🤖 Integración de ChatGPT - Asistente Virtual AI

## 📋 Configuración Inicial

### 1. Obtener API Key de OpenAI
1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión en tu cuenta de OpenAI
3. Crea una nueva API key
4. Copia la key (empieza con `sk-`)

### 2. Configurar la API Key

**Opción A - Archivo .env (Recomendado):**
```bash
# Edita el archivo .env
OPENAI_API_KEY=tu_api_key_aqui
```

**Opción B - Interfaz de usuario:**
- En cualquier página del asistente, ve al sidebar
- Ingresa tu API key en el campo "OpenAI API Key"
- Haz clic en "Conectar AI"

## ⚙️ Configuración Optimizada por Módulo

El sistema utiliza **gpt-4o-mini** con configuraciones específicas optimizadas para cada funcionalidad:

```python
MODEL_CONFIG = {
    "minutas": {
        "model": "gpt-4o-mini",
        "temperature": 0.25,      # Más preciso para extraer información
        "max_tokens": 2000        # Más espacio para minutas detalladas
    },
    "1to1": {
        "model": "gpt-4o-mini", 
        "temperature": 0.4,       # Balance entre precisión y creatividad
        "max_tokens": 1000        # Respuestas concisas para coaching
    },
    "competidores": {
        "model": "gpt-4o-mini",
        "temperature": 0.3,       # Análisis objetivo
        "max_tokens": 1500        # Análisis detallado pero enfocado
    },
    "clientes": {
        "model": "gpt-4o-mini",
        "temperature": 0.35,      # Insights balanceados
        "max_tokens": 1800        # Reportes ejecutivos completos
    }
}
```

## 🚀 Funcionalidades AI Integradas

### 📝 Generación de Minutas
- **Configuración:** Temperatura 0.25, 2000 tokens
- **Optimizado para:** Extracción precisa de información estructurada
- **Ubicación:** Página "Generar Minutas" → Sección "🤖 Mejora con AI"
- **Uso:** 
  1. Pega la transcripción de tu reunión
  2. Añade contexto opcional
  3. Haz clic en "Generar con AI"
  4. Obtén objetivos, resumen, acuerdos y tareas estructuradas

### 📊 Análisis de Competidores
- **Configuración:** Temperatura 0.3, 1500 tokens
- **Optimizado para:** Análisis objetivo y estructurado
- **Ubicación:** Página "Radar de Competidores" (funcionalidad integrada)
- **Genera:**
  - Resumen ejecutivo
  - Fortalezas identificadas
  - Debilidades y oportunidades
  - Recomendaciones estratégicas

### 📈 Insights de Clientes
- **Configuración:** Temperatura 0.35, 1800 tokens
- **Optimizado para:** Reportes ejecutivos completos
- **Ubicación:** Página "Reporte Clientes Trimestral" → Sección "🤖 Insights con AI"
- **Genera:**
  - Análisis de tendencias
  - Oportunidades de crecimiento
  - Evaluación de riesgos
  - Recomendaciones estratégicas
  - Próximos pasos

### 👥 Preparación de Reuniones 1:1
- **Configuración:** Temperatura 0.4, 1000 tokens
- **Optimizado para:** Coaching empático y constructivo
- **Ubicación:** Página "Reuniones 1:1" (funcionalidad integrada)
- **Genera:**
  - Temas prioritarios a discutir
  - Preguntas de seguimiento sugeridas
  - Objetivos de desarrollo
  - Acciones de apoyo
  - Preparación para próxima reunión

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)
```bash
# Configuración por defecto (se sobrescribe por módulo)
DEFAULT_MODEL=gpt-4o-mini
DEFAULT_MAX_TOKENS=1500
DEFAULT_TEMPERATURE=0.3
```

### ¿Por qué gpt-4o-mini?
- **Costo-efectivo:** Significativamente más barato que GPT-4
- **Rápido:** Respuestas más veloces
- **Preciso:** Excelente para tareas estructuradas
- **Optimizado:** Configuraciones específicas por caso de uso

## 🔒 Seguridad

- ✅ Las API keys se almacenan de forma segura
- ✅ El archivo `.env` está en `.gitignore`
- ✅ No se envían datos sensibles sin tu consentimiento
- ✅ Todas las funciones AI son opcionales
- ✅ Configuraciones optimizadas para minimizar costos

## 🆘 Solución de Problemas

### Error: "No se encontró la API key"
- Verifica que tu API key esté correctamente configurada
- Asegúrate de que empiece con `sk-`
- Revisa que no tenga espacios extra

### Error: "Error al conectar con OpenAI"
- Verifica tu conexión a internet
- Confirma que tu API key sea válida
- Revisa que tengas créditos disponibles en OpenAI

### Las funciones AI no aparecen
- Asegúrate de haber conectado tu API key
- Verifica que aparezca "✅ OpenAI conectado" en el sidebar

## 💡 Tips de Uso

1. **Sé específico:** Proporciona contexto detallado para mejores resultados
2. **Revisa siempre:** El AI es una herramienta de apoyo, siempre revisa los resultados
3. **Experimenta:** Cada módulo está optimizado para su caso de uso específico
4. **Combina:** Usa las funciones AI junto con tus conocimientos expertos
5. **Costo-consciente:** Las configuraciones están optimizadas para minimizar costos

## 📊 Información de Configuración

Cada módulo muestra su configuración específica en el sidebar cuando AI está conectado:
- **Modelo utilizado**
- **Temperatura configurada** 
- **Tokens máximos**

## 📞 Soporte

Si tienes problemas con la integración de AI:
1. Revisa esta documentación
2. Verifica la configuración de tu API key
3. Consulta los logs de error en la interfaz