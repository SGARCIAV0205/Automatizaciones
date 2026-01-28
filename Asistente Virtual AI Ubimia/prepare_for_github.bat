@echo off
echo ========================================
echo   PREPARANDO PARA STREAMLIT CLOUD
echo ========================================

echo.
echo 1. Inicializando repositorio Git...
git init

echo.
echo 2. Agregando archivos...
git add .

echo.
echo 3. Creando commit inicial...
git commit -m "Initial commit - Asistente Virtual AI con autenticacion"

echo.
echo 4. Configurando rama principal...
git branch -M main

echo.
echo ========================================
echo   LISTO PARA SUBIR A GITHUB
echo ========================================
echo.
echo PROXIMOS PASOS:
echo 1. Crea un repositorio en GitHub (publico para plan gratuito)
echo 2. Ejecuta: git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
echo 3. Ejecuta: git push -u origin main
echo 4. Ve a https://share.streamlit.io/ y conecta tu repositorio
echo.
echo CREDENCIALES DE ACCESO:
echo Usuario: ubimia_admin
echo Contraseña: UbimiaAI2024!
echo.
pause