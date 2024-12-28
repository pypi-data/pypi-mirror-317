# Changelog

## [0.2.6] - 2024-12-27

### Added
- Implementación completa de operaciones tipo Prisma:
  - findUnique
  - findFirst
  - findMany
  - create
  - update
  - upsert
  - delete
  - count
  - aggregate
- Soporte mejorado para consultas SQL con schema

### Changed
- Eliminada la opción redundante de `options` en favor de parámetros directos
- Mejorada la construcción de queries SQL para manejar correctamente schemas y tablas
- Refactorización de la clase Table para una API más limpia

### Fixed
- Corregido el manejo de schemas en consultas SQL
- Arreglada la inicialización de tablas en el cliente 