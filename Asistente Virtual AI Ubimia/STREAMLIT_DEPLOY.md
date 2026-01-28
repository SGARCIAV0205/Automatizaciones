# 🚀 Despliegue en Streamlit Cloud (GRATUITO)

## 🌟 **Ventajas de Streamlit Cloud**
- ✅ **100% Gratuito** para proyectos públicos
- ✅ **Despliegue automático** desde GitHub
- ✅ **Sin límites de tiempo** (a diferencia de Heroku)
- ✅ **SSL automático** (HTTPS)
- ✅ **Actualizaciones automáticas** al hacer push

## 📋 **Pasos para Desplegar**

### **1. Subir Código a GitHub**

1. **Crear repositorio en GitHub:**
   - Ve a https://github.com/new
   - Nombre: `asistente-virtual-ai`
   - Tipo: **Público** (para plan gratuito)
   - ✅ Add README file

2. **Subir tu código:**
   ```bash
   # En la carpeta "Asistente Virtual AI Ubimia"
   git init
   git add .
   git commit -m "Initial commit - Asistente Virtual AI"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/asistente-virtual-ai.git
   git push -u origin main
   ```

### **2. Configurar Streamlit Cloud**

1. **Ir a Streamlit Cloud:**
   - Ve a https://share.streamlit.io/
   - Haz clic en "Sign up" o "Sign in"
   - Conecta tu cuenta de GitHub

2. **Crear nueva app:**
   - Clic en "New app"
   - **Repository:** `TU_USUARIO/asistente-virtual-ai`
   - **Branch:** `main`
   - **Main file path:** `Inicio.py`
   - **App URL:** `asistente-virtual-ai` (o el que prefieras)

### **3. Configurar Variables de Entorno (Secretos)**

En Streamlit Cloud, ve a tu app → "Settings" → "Secrets" y agrega:

```toml
# Configuración de autenticación
APP_USERNAME = "ubimia_admin"
APP_PASSWORD = "UbimiaAI2024!"

# Configuración de OpenAI
OPENAI_API_KEY = "sk-proj-tu_api_key_aqui"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MAX_TOKENS = "1500"
DEFAULT_TEMPERATURE = "0.3"
```

### **4. ¡Listo! Tu App Está Online**

- URL: `https://asistente-virtual-ai.streamlit.app/`
- **Usuario:** `ubimia_admin`
- **Contraseña:** `UbimiaAI2024!`

## 🔄 **Actualizaciones Automáticas**

Cada vez que hagas `git push` a tu repositorio, Streamlit Cloud automáticamente:
1. Detecta los cambios
2. Redespliega la aplicación
3. Actualiza la URL en vivo

```bash
# Para actualizar tu app
git add .
git commit -m "Actualización de funcionalidades"
git push
```

## 🔒 **Configuración de Seguridad**

### **Cambiar Credenciales:**
1. Ve a Streamlit Cloud → Tu App → Settings → Secrets
2. Modifica:
   ```toml
   APP_USERNAME = "tu_nuevo_usuario"
   APP_PASSWORD = "tu_nueva_contraseña_segura"
   ```
3. Guarda los cambios (la app se reinicia automáticamente)

### **Hacer Repositorio Privado (Opcional):**
- Requiere plan de pago de GitHub
- Streamlit Cloud sigue siendo gratuito
- Mayor seguridad para tu código

## 📊 **Límites del Plan Gratuito**

- ✅ **Apps ilimitadas**
- ✅ **Usuarios ilimitados**
- ✅ **Ancho de banda ilimitado**
- ⚠️ **Recursos compartidos** (puede ser más lento en horas pico)
- ⚠️ **Apps inactivas se "duermen"** (se reactivan al acceder)

## 🆘 **Solución de Problemas**

### **Error: "Module not found"**
- Verifica que `requirements.txt` esté completo
- Ejecuta localmente: `pip freeze > requirements.txt`

### **Error: "Secrets not found"**
- Ve a Settings → Secrets en Streamlit Cloud
- Verifica que todas las variables estén configuradas

### **App muy lenta:**
- Normal en plan gratuito durante horas pico
- Considera optimizar el código para usar menos recursos

### **App se "duerme":**
- Normal después de inactividad
- Se reactiva automáticamente al acceder
- Para mantenerla activa 24/7, considera plan de pago

## 💡 **Tips para Optimizar**

1. **Usar st.cache_data** para datos que no cambian frecuentemente
2. **Minimizar imports** pesados
3. **Optimizar imágenes** y archivos estáticos
4. **Usar session_state** eficientemente

## 🔗 **Enlaces Útiles**

- **Streamlit Cloud:** https://share.streamlit.io/
- **Documentación:** https://docs.streamlit.io/streamlit-cloud
- **Comunidad:** https://discuss.streamlit.io/

## 📞 **Soporte**

Si tienes problemas:
1. Revisa los logs en Streamlit Cloud
2. Consulta la documentación oficial
3. Pregunta en el foro de la comunidad

---

## 🎯 **Resumen Rápido**

1. **Sube código a GitHub** (repositorio público)
2. **Conecta Streamlit Cloud** con tu repositorio
3. **Configura secretos** (API keys, credenciales)
4. **¡Tu app está online y es GRATUITA!**

**URL final:** `https://tu-app-name.streamlit.app/`