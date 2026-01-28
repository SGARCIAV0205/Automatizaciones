# 🤖 Automatizaciones - Asistente Virtual AI

Sistema completo de automatizaciones empresariales con interfaz web y funcionalidades de IA.

## 🌟 **Características Principales**

- 🔐 **Autenticación segura** con usuario y contraseña
- 🤖 **Integración con ChatGPT** (gpt-4o-mini optimizado)
- 📝 **Generación de minutas** automática desde transcripciones
- 📊 **Análisis de competidores** con insights de IA
- 📈 **Reportes de clientes** trimestrales con análisis automático
- 👥 **Gestión de reuniones 1:1** con preparación inteligente
- 📄 **Template Writer** para documentos automatizados

## 🚀 **Acceso a la Aplicación**

**URL:** [https://automatizaciones-ubimia.streamlit.app/](https://automatizaciones-ubimia.streamlit.app/)

### 🔑 **Credenciales de Acceso**
- **Usuario:** `ubimia_admin`
- **Contraseña:** `UbimiaAI2024!`

## 🛠 **Tecnologías Utilizadas**

- **Frontend:** Streamlit
- **Backend:** Python 3.9+
- **IA:** OpenAI GPT-4o-mini
- **Hosting:** Streamlit Cloud (Gratuito)
- **Autenticación:** Sistema personalizado con hash SHA-256

## 📋 **Módulos Incluidos**

### 1. **Asistente Virtual AI Ubimia** (Interfaz Principal)
- Dashboard central con acceso a todos los módulos
- Sistema de autenticación integrado
- Configuración de IA por módulo

### 2. **Generación de Minutas**
- Conversión de transcripciones a minutas estructuradas
- Extracción automática de objetivos, acuerdos y tareas
- Exportación a DOCX y Markdown

### 3. **Radar de Competidores**
- Monitoreo de competidores
- Análisis de fortalezas y debilidades
- Generación de reportes PPTX

### 4. **Reporte Clientes Trimestral**
- Análisis de datos de clientes
- Insights automáticos con IA
- Presentaciones ejecutivas

### 5. **Reuniones 1:1**
- Gestión de reuniones individuales
- Preparación automática con IA
- Seguimiento de compromisos

### 6. **Template Writer**
- Generación de documentos desde plantillas
- Configuración flexible
- Múltiples formatos de salida

## ⚙️ **Configuración de IA por Módulo**

```python
MODEL_CONFIG = {
    "minutas": {"temperature": 0.25, "max_tokens": 2000},      # Precisión
    "1to1": {"temperature": 0.4, "max_tokens": 1000},         # Balance
    "competidores": {"temperature": 0.3, "max_tokens": 1500}, # Objetivo
    "clientes": {"temperature": 0.35, "max_tokens": 1800}     # Insights
}
```

## 🔒 **Seguridad**

- ✅ Autenticación obligatoria en todas las páginas
- ✅ Contraseñas hasheadas con SHA-256
- ✅ Variables de entorno para credenciales
- ✅ API keys protegidas
- ✅ Sesiones seguras

## 📱 **Uso**

1. **Accede** a la URL de la aplicación
2. **Inicia sesión** con las credenciales proporcionadas
3. **Configura** tu API key de OpenAI (opcional, para funciones de IA)
4. **Selecciona** el módulo que necesites usar
5. **Disfruta** de las automatizaciones

## 🔧 **Desarrollo Local**

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/automatizaciones.git
cd automatizaciones

# Instalar dependencias
pip install -r "Asistente Virtual AI Ubimia/requirements.txt"

# Configurar variables de entorno
cp "Asistente Virtual AI Ubimia/.env.example" "Asistente Virtual AI Ubimia/.env"
# Editar .env con tus credenciales

# Ejecutar aplicación
streamlit run "Asistente Virtual AI Ubimia/Inicio.py"
```

## 📊 **Estructura del Proyecto**

```
automatizaciones/
├── Asistente Virtual AI Ubimia/    # Interfaz principal
│   ├── Inicio.py                   # Punto de entrada
│   ├── pages/                      # Páginas de la aplicación
│   ├── modules/                    # Módulos compartidos
│   └── assets/                     # Recursos estáticos
├── Generación de Minutas/          # Módulo de minutas
├── Radar Competidores/             # Módulo de competidores
├── Reporte Clientes Trimestral/    # Módulo de reportes
├── 1to1/                          # Módulo de reuniones 1:1
└── Template Writer/               # Módulo de plantillas
```

## 🆘 **Soporte**

Para problemas o consultas:
1. Revisa la documentación en cada módulo
2. Verifica la configuración de variables de entorno
3. Consulta los logs de la aplicación

## 📄 **Licencia**

Proyecto privado - Todos los derechos reservados.

---

**Desarrollado con ❤️ para automatizar y optimizar procesos empresariales.**