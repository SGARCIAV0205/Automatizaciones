# Configuración de Supabase (Base de Datos Gratuita)

## 1. Crear cuenta en Supabase

1. Ve a [supabase.com](https://supabase.com)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto
4. Anota la **URL** y **anon key** del proyecto

## 2. Crear las tablas necesarias

Ejecuta estos comandos SQL en el editor SQL de Supabase:

```sql
-- Tabla para clientes (Reporte Clientes Trimestral)
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    sector VARCHAR(255),
    keywords TEXT, -- JSON array como string
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Tabla para competidores (Radar Competidores)
CREATE TABLE competidores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    notas TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Tabla para configuración del radar
CREATE TABLE configuracion_radar (
    clave VARCHAR(100) PRIMARY KEY,
    valor TEXT,
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

-- Tabla para participantes 1to1
CREATE TABLE participantes_1to1 (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    objetivos_anuales TEXT,
    fortalezas TEXT,
    oportunidades_mejora TEXT,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Tabla para historial de reuniones 1to1
CREATE TABLE historial_1to1 (
    id SERIAL PRIMARY KEY,
    id_participante INTEGER REFERENCES participantes_1to1(id),
    fecha_reunion DATE,
    objetivos_reunion TEXT,
    puntos_discutidos TEXT,
    insight_coaching TEXT,
    notas_reunion TEXT,
    compromisos TEXT, -- JSON array como string
    fecha_proxima_reunion DATE,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

-- Insertar configuración inicial del radar
INSERT INTO configuracion_radar (clave, valor) VALUES
('periodo', '2025-01'),
('use_llm', 'false'),
('openai_model', 'gpt-4o-mini'),
('notas_globales', '');
```

## 3. Configurar en Streamlit Cloud

En el dashboard de Streamlit Cloud, ve a **Settings > Secrets** y agrega:

```toml
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_ANON_KEY = "tu-anon-key-aqui"
```

## 4. Configurar para desarrollo local

Crea un archivo `.env` en la raíz del proyecto:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu-anon-key-aqui
```

## 5. Verificar funcionamiento

1. Reinicia la aplicación en Streamlit Cloud
2. Ve a cualquier módulo (Reporte Clientes, Radar, 1to1)
3. Si está conectado correctamente, los datos se persistirán entre reinicios
4. Si hay problemas, la app seguirá funcionando con almacenamiento local temporal

## Límites del plan gratuito de Supabase:

- ✅ 500MB de base de datos
- ✅ 50MB de almacenamiento de archivos  
- ✅ 2GB de transferencia de datos
- ✅ 50,000 usuarios autenticados
- ✅ Hasta 2 proyectos

**Más que suficiente para esta aplicación.**

## Beneficios:

- 🔄 **Datos persistentes** entre reinicios de Streamlit Cloud
- 🚀 **Sin cambios en el código** existente (100% compatible)
- 💰 **Completamente gratuito**
- 🔒 **Seguro** (PostgreSQL en la nube)
- 📊 **Dashboard web** para ver/editar datos
- 🔄 **Backups automáticos**

## Troubleshooting:

- Si no se conecta: Verifica URL y anon key en secrets
- Si faltan tablas: Ejecuta el SQL de creación de tablas
- Si hay errores: La app seguirá funcionando con almacenamiento local
- Para debugging: Activa "Mostrar estado BD" en el sidebar