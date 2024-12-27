# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.9] - 2024-03-14

### Cambiado
- Mejorado el sistema de carga de configuración para soportar múltiples ubicaciones
- Agregada la opción de especificar ruta explícita del archivo de configuración
- Actualizado el CLI para guardar la configuración en la raíz del proyecto

## [0.1.8] - 2024-03-14

### Cambiado
- Mejorada la búsqueda del archivo de configuración para usar la ruta absoluta del proyecto
- Actualizada la lógica de carga de configuración para ser más robusta

## [0.1.7] - 2024-03-14

### Cambiado
- Mejorada la búsqueda del archivo de configuración para usar la ruta absoluta del proyecto
- Actualizada la lógica de carga de configuración para ser más robusta

## [0.1.6] - 2024-03-14

### Cambiado
- Reorganizada la estructura del proyecto para seguir mejores prácticas
- Corregidas las importaciones relativas en todos los módulos
- Unificadas las versiones en todos los archivos del proyecto

### Corregido
- Solucionado el problema de importación del módulo principal
- Mejorada la estructura de directorios para una correcta instalación del paquete

## [0.1.5] - 2024-03-14

### Corregido
- Solucionado el problema con el event loop de asyncio durante la introspección
- Eliminada la pregunta duplicada sobre la ubicación de los stubs
- Mejorado el manejo de la generación de stubs

## [0.1.4] - 2024-03-14

### Cambiado
- Actualizada la ubicación por defecto de los stubs a la carpeta raíz del proyecto
- Agregada opción interactiva para elegir la ubicación de los stubs durante la inicialización
- Mejorada la configuración para incluir la ubicación de los stubs
- Corregida la estructura del paquete para permitir una correcta instalación del CLI
- Movido el CLI a una ubicación más estándar dentro del paquete

## [0.1.3] - 2024-03-14

### Cambiado
- Actualizada la URL del repositorio a Bitbucket
- Mejorada la documentación y referencias en los archivos de configuración

## [0.1.2] - 2024-03-14

### Corregido
- Arreglado el problema con la importación del módulo helpers
- Mejorada la configuración de paquetes en setup.py

## [0.1.1] - 2024-03-14

### Corregido
- Arreglado el problema con el punto de entrada del CLI
- Corregido el manejo de configuración del logger

### Cambiado
- Mejorada la estructura del paquete para una mejor instalación
- Actualizada la documentación

## [0.1.0] - 2024-03-14

### Agregado
- Versión inicial del proyecto
- Soporte para PostgreSQL y MySQL
- Sistema de caché con soporte para memoria y Redis
- CLI para inicialización y gestión
- Introspección automática de bases de datos
- Generación automática de modelos 