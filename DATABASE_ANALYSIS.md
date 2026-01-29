# Análisis de Necesidades de Base de Datos Externa

## Módulos que NECESITAN base de datos externa:

### 1. **Reporte Clientes Trimestral** 🔴 CRÍTICO
- **Archivo actual**: `Reporte Clientes Trimestral/rt_utils/client_store.py`
- **Datos que se pierden**: 
  - Lista de clientes (`clientes.json`)
  - Información de clientes (nombre, sector, keywords)
- **Impacto**: Los usuarios tienen que volver a agregar clientes cada vez que se reinicia
- **Solución requerida**: Base de datos para persistir catálogo de clientes

### 2. **Radar Competidores** 🔴 CRÍTICO  
- **Archivo actual**: `Radar Competidores/config.yaml`
- **Datos que se pierden**:
  - Lista de competidores
  - Notas por competidor
  - Configuración de períodos
  - Parámetros LLM personalizados
- **Impacto**: Configuración completa se pierde en cada reinicio
- **Solución requerida**: Base de datos para configuración y datos de competidores

### 3. **Reuniones 1to1** 🔴 CRÍTICO
- **Archivos actuales**: 
  - `1to1/data/participantes.csv`
  - `1to1/data/historial_1to1.csv`
- **Datos que se pierden**:
  - Lista de participantes/empleados
  - Historial completo de reuniones 1:1
  - Compromisos y seguimientos
  - Objetivos anuales y evaluaciones
- **Impacto**: Se pierde todo el historial de reuniones y seguimiento de empleados
- **Solución requerida**: Base de datos para participantes e historial de reuniones

## Módulos que NO necesitan base de datos externa:

### 4. **Generar Minutas** 🟢 OK
- **Razón**: Solo genera archivos de salida (PDF, DOCX, JSON)
- **Datos**: No mantiene estado entre sesiones
- **Funcionamiento**: Cada minuta es independiente

### 5. **Template Writer** 🟢 OK  
- **Razón**: Solo genera documentos basados en plantillas
- **Datos**: No mantiene estado entre sesiones
- **Funcionamiento**: Cada documento es independiente

## Recomendaciones de Implementación:

### Opción 1: Base de Datos Simple (Recomendada para MVP)
- **SQLite** con tablas:
  - `clientes` (id, nombre, sector, keywords, fecha_creacion)
  - `competidores` (id, nombre, notas, activo)
  - `configuracion_radar` (clave, valor)
  - `participantes_1to1` (id, nombre, email, objetivos, fortalezas)
  - `historial_1to1` (id, participante_id, fecha, notas, compromisos)

### Opción 2: Base de Datos en la Nube
- **Supabase** (PostgreSQL gratuito)
- **Firebase Firestore**
- **MongoDB Atlas**

### Opción 3: Almacenamiento de Archivos Persistente
- **Google Drive API**
- **Dropbox API**
- **AWS S3**

## Prioridad de Implementación:

1. **Reuniones 1to1** - Más crítico (historial de empleados)
2. **Reporte Clientes Trimestral** - Medio (catálogo de clientes)
3. **Radar Competidores** - Medio (configuración de competidores)

## Impacto Actual:
- Los usuarios pierden toda la información cada vez que Streamlit Cloud reinicia la aplicación
- Experiencia de usuario muy pobre al tener que reconfigurar todo constantemente
- Pérdida de valor del historial y seguimiento a largo plazo