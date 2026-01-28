# 🚀 Guía de Despliegue en Google Cloud

## 📋 Credenciales Configuradas

**Usuario:** `ubimia_admin`  
**Contraseña:** `UbimiaAI2024!`

## 🔧 Preparación para Despliegue

### 1. Instalar Google Cloud CLI
```bash
# Descargar e instalar desde: https://cloud.google.com/sdk/docs/install
gcloud auth login
gcloud config set project TU_PROJECT_ID
```

### 2. Configurar Variables de Entorno Seguras

**Opción A - Usar Google Secret Manager (Recomendado):**
```bash
# Crear secretos
gcloud secrets create openai-api-key --data-file=<(echo "tu_openai_api_key")
gcloud secrets create app-password --data-file=<(echo "UbimiaAI2024!")

# Dar permisos a App Engine
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
    --member="serviceAccount:TU_PROJECT_ID@appspot.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

**Opción B - Variables de entorno directas:**
Edita `app.yaml` y agrega tu OPENAI_API_KEY:
```yaml
env_variables:
  OPENAI_API_KEY: "tu_openai_api_key_aqui"
  APP_USERNAME: "ubimia_admin"
  APP_PASSWORD: "UbimiaAI2024!"
```

### 3. Generar Hash de Contraseña (Opcional, más seguro)
```bash
python generate_password_hash.py
# Copia el hash generado y úsalo en lugar de APP_PASSWORD
```

## 🚀 Despliegue

### Opción 1 - App Engine (Recomendado)
```bash
# Desde el directorio "Asistente Virtual AI Ubimia"
gcloud app deploy app.yaml

# Ver logs
gcloud app logs tail -s default

# Abrir en navegador
gcloud app browse
```

### Opción 2 - Cloud Run
```bash
# Construir imagen
gcloud builds submit --tag gcr.io/TU_PROJECT_ID/asistente-virtual

# Desplegar
gcloud run deploy asistente-virtual \
    --image gcr.io/TU_PROJECT_ID/asistente-virtual \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="APP_USERNAME=ubimia_admin,APP_PASSWORD=UbimiaAI2024!"
```

## 🔒 Configuración de Seguridad

### 1. Cambiar Credenciales por Defecto
Antes del despliegue, cambia las credenciales en `app.yaml`:
```yaml
env_variables:
  APP_USERNAME: "tu_usuario_personalizado"
  APP_PASSWORD: "tu_contraseña_super_segura"
```

### 2. Usar HTTPS (Automático en Google Cloud)
Google Cloud automáticamente proporciona certificados SSL.

### 3. Configurar Firewall (Opcional)
```bash
# Restringir acceso por IP
gcloud app firewall-rules create 1000 --action allow --source-range="TU_IP/32"
gcloud app firewall-rules create 2000 --action deny --source-range="*"
```

## 🌐 Acceso a la Aplicación

Una vez desplegada:
1. Ve a la URL proporcionada por Google Cloud
2. Ingresa las credenciales:
   - **Usuario:** `ubimia_admin`
   - **Contraseña:** `UbimiaAI2024!`
3. ¡Disfruta tu Asistente Virtual AI!

## 📊 Monitoreo

### Ver Logs
```bash
gcloud app logs tail -s default
```

### Métricas
- Ve a Google Cloud Console → App Engine → Monitoring
- Revisa CPU, memoria y requests

## 🔧 Mantenimiento

### Actualizar Aplicación
```bash
gcloud app deploy app.yaml
```

### Cambiar Credenciales
1. Edita `app.yaml`
2. Redespliega: `gcloud app deploy app.yaml`

### Backup de Datos
Los datos de sesión se almacenan en memoria. Para persistencia, considera usar:
- Google Cloud Firestore
- Google Cloud SQL
- Google Cloud Storage

## 🆘 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` incluya todas las dependencias
- Ejecuta `pip freeze > requirements.txt` localmente

### Error: "Authentication failed"
- Verifica las variables de entorno en `app.yaml`
- Revisa los logs: `gcloud app logs tail -s default`

### Error: "OpenAI API"
- Confirma que OPENAI_API_KEY esté configurada
- Verifica que tengas créditos en OpenAI

## 💰 Costos Estimados

**App Engine:**
- Instancia F1: ~$0.05/hora
- Tráfico: ~$0.12/GB
- **Estimado mensual:** $30-50 USD (uso moderado)

**Cloud Run:**
- CPU: $0.00002400/vCPU-second
- Memoria: $0.00000250/GiB-second
- **Estimado mensual:** $10-30 USD (uso moderado)

## 🔐 Credenciales de Acceso

**Para cambiar las credenciales por defecto:**

1. **Edita el archivo `.env` o `app.yaml`**
2. **Cambia:**
   ```
   APP_USERNAME=tu_nuevo_usuario
   APP_PASSWORD=tu_nueva_contraseña_segura
   ```
3. **Redespliega la aplicación**

**Credenciales actuales:**
- Usuario: `ubimia_admin`
- Contraseña: `UbimiaAI2024!`