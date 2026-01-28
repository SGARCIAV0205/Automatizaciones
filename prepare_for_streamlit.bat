@echo off
echo ========================================
echo   PREPARANDO TODO EL PROYECTO PARA
echo        STREAMLIT CLOUD
echo ========================================

echo.
echo 1. Inicializando repositorio Git en la raiz...
git init

echo.
echo 2. Agregando todos los archivos del proyecto...
git add .

echo.
echo 3. Creando commit inicial...
git commit -m "Initial commit - Automatizaciones completas con Asistente Virtual AI"

echo.
echo 4. Configurando rama principal...
git branch -M main

echo.
echo ========================================
echo   LISTO PARA SUBIR A GITHUB
echo ========================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Crea un repositorio en GitHub:
echo    - Ve a https://github.com/new
echo    - Nombre: automatizaciones-ubimia
echo    - Tipo: PUBLICO (para plan gratuito de Streamlit)
echo    - NO marques "Add README file"
echo.
echo 2. Conecta y sube el repositorio:
echo    git remote add origin https://github.com/TU_USUARIO/automatizaciones-ubimia.git
echo    git push -u origin main
echo.
echo 3. Configura Streamlit Cloud:
echo    - Ve a https://share.streamlit.io/
echo    - New app ^> Connect repository
echo    - Repository: TU_USUARIO/automatizaciones-ubimia
echo    - Branch: main
echo    - Main file path: Asistente Virtual AI Ubimia/Inicio.py
echo    - App URL: automatizaciones-ubimia
echo.
echo 4. Configura los secretos en Streamlit Cloud:
echo    Settings ^> Secrets ^> Agregar:
echo    APP_USERNAME = "ubimia_admin"
echo    APP_PASSWORD = "UbimiaAI2024!"
echo    OPENAI_API_KEY = "tu_api_key_aqui"
echo    DEFAULT_MODEL = "gpt-4o-mini"
echo    DEFAULT_MAX_TOKENS = "1500"
echo    DEFAULT_TEMPERATURE = "0.3"
echo.
echo ========================================
echo   CREDENCIALES DE ACCESO FINAL
echo ========================================
echo Usuario: ubimia_admin
echo Contraseña: UbimiaAI2024!
echo URL: https://automatizaciones-ubimia.streamlit.app/
echo.
pause