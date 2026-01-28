@echo off
echo ========================================
echo   ARREGLANDO DESPLIEGUE DE STREAMLIT
echo ========================================

echo.
echo 1. Copiando requirements.txt a la ubicacion correcta...
copy "requirements.txt" "Asistente Virtual AI Ubimia\requirements.txt"

echo.
echo 2. Agregando cambios...
git add .

echo.
echo 3. Creando commit de arreglo...
git commit -m "Fix: Mover requirements.txt para Streamlit Cloud"

echo.
echo 4. Subiendo cambios...
git push

echo.
echo ========================================
echo   CAMBIOS SUBIDOS
echo ========================================
echo.
echo Streamlit Cloud detectara automaticamente los cambios
echo y reiniciara la aplicacion en unos minutos.
echo.
echo Si el problema persiste:
echo 1. Ve a tu app en Streamlit Cloud
echo 2. Settings ^> Reboot app
echo 3. O cambia la configuracion:
echo    Main file path: Asistente Virtual AI Ubimia/Inicio.py
echo.
pause