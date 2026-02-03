# Módulo: Generación de Minutas

## 🎯 Propósito y Necesidades que Cubre

### Problema que Resuelve
- **Tiempo perdido**: Las minutas manuales consumen 30-60 minutos por reunión
- **Inconsistencia**: Diferentes formatos y niveles de detalle entre equipos
- **Información perdida**: Puntos importantes que se olvidan o no se documentan
- **Seguimiento deficiente**: Tareas y compromisos que no se trackean adecuadamente

### Valor Agregado
- **Ahorro de tiempo**: Reduce de 45 minutos a 5 minutos el proceso de documentación
- **Estandarización**: Formato consistente y profesional en todas las minutas
- **Trazabilidad**: Seguimiento automático de decisiones, tareas y compromisos
- **Inteligencia**: Extracción automática de insights y riesgos de las conversaciones

## ⚙️ Funcionalidades Principales

### 1. Procesamiento Inteligente de Transcripciones
- Acepta múltiples formatos: `.txt`, `.docx`, `.srt`, `.vtt`
- Chunking inteligente basado en tokens para optimizar procesamiento
- Análisis semántico con modelos GPT-4o y GPT-4o-mini

### 2. Extracción Estructurada de Información
- **Decisiones tomadas** con responsables e impacto
- **Acuerdos alcanzados** con fechas y responsables
- **Tareas asignadas** con metodología SMART
- **Riesgos identificados** con probabilidad y mitigación
- **Próximos pasos** con dueños y fechas

### 3. Generación Multi-formato
- **Markdown** para revisión y edición
- **PDF** para distribución formal
- **JSON** para integración con sistemas
- **DOCX** para edición colaborativa

## 📊 Ejemplo de Output

### Input: Transcripción de Reunión
```
"Buenas tardes equipo. Hoy vamos a revisar el avance del proyecto CRM. 
María, ¿cómo va la integración con Salesforce?"

"Hola a todos. La integración va bien, pero tenemos un retraso de 3 días 
por problemas con la API. Necesitamos que TI nos dé acceso a los logs."

"Perfecto. Juan, ¿puedes coordinar eso para mañana? También decidimos 
que vamos a cambiar el proveedor de hosting por temas de costos."
```

### Output: Minuta Estructurada

```markdown
# Minuta de Reunión - Proyecto CRM

**Proyecto:** Implementación CRM  
**Fecha:** 2025-02-02  

## Participantes
- **María González** (maria.gonzalez@ubimia.com) - Líder Técnico
- **Juan Pérez** (juan.perez@ubimia.com) - Coordinador TI

## Resumen Ejecutivo
Reunión de seguimiento del proyecto CRM. Se identificó retraso en integración con Salesforce por problemas de API. Se tomó decisión estratégica sobre cambio de proveedor de hosting.

## Decisiones Tomadas
- Cambio de proveedor de hosting por optimización de costos
  - Responsable: Equipo de infraestructura
  - Impacto: Alto - Reducción de costos operativos

## Tareas Asignadas
- **Coordinar acceso a logs de API Salesforce**
  - Responsable: Juan Pérez
  - Fecha límite: 2025-02-03
  - Métrica: Acceso completo a logs habilitado

## Riesgos Identificados
- Retraso en integración Salesforce (3 días)
  - Probabilidad: Alta
  - Impacto: Medio
  - Mitigación: Acceso prioritario a logs y soporte técnico
  - Dueño: María González

## Próximos Pasos
- Evaluar proveedores alternativos de hosting
  - Dueño: Equipo de infraestructura
  - Fecha: 2025-02-05
```

## 🎯 Casos de Uso Típicos

### 1. Reuniones de Seguimiento de Proyectos
- **Frecuencia**: Semanal/Quincenal
- **Participantes**: 3-8 personas
- **Duración**: 30-60 minutos
- **Beneficio**: Trazabilidad completa de avances y blockers

### 2. Reuniones de Comité Directivo
- **Frecuencia**: Mensual
- **Participantes**: 5-12 ejecutivos
- **Duración**: 60-120 minutos
- **Beneficio**: Documentación formal de decisiones estratégicas

### 3. Reuniones de Planificación Sprint
- **Frecuencia**: Cada 2 semanas
- **Participantes**: Equipo de desarrollo (5-10 personas)
- **Duración**: 45-90 minutos
- **Beneficio**: Seguimiento automático de compromisos y dependencias

### 4. Reuniones Cliente-Proveedor
- **Frecuencia**: Variable
- **Participantes**: 2-6 personas
- **Duración**: 30-90 minutos
- **Beneficio**: Documentación profesional para compliance y seguimiento

## 📈 Métricas de Impacto

- **Tiempo ahorrado**: 85% reducción en tiempo de documentación
- **Consistencia**: 100% de minutas con formato estandarizado
- **Seguimiento**: 95% de tareas con responsable y fecha asignada
- **Satisfacción**: Incremento del 40% en satisfacción con proceso de reuniones

## 🔧 Configuración Recomendada

### Para Reuniones Cortas (≤30 min)
- **Tokens por bloque**: 800-1200
- **Modelo Map**: gpt-4o-mini
- **Modelo Reduce**: gpt-4o

### Para Reuniones Largas (>60 min)
- **Tokens por bloque**: 2500-3500
- **Modelo Map**: gpt-4o-mini
- **Modelo Reduce**: gpt-4o

---
*Módulo desarrollado por Ubimia para optimización de procesos de reuniones*