# Changelog

## [0.2.10] - 2024-12-27

### Added
- Nueva funcionalidad createMany para inserciones masivas
  - Soporte para inserción de múltiples registros en una sola operación
  - Opción skipDuplicates para ignorar registros duplicados
  - Validación de consistencia en las columnas

## [0.2.9] - 2024-12-27

### Fixed
- Corrección en la validación de operadores de agregación
- Unificación de operadores de agregación en validator.py
- Soporte mejorado para COUNT en agregaciones

## [0.2.8] - 2024-12-27

### Added
- Soporte para operadores de comparación en consultas WHERE
  - Nuevos operadores: gt, gte, lt, lte, in, notIn, contains, notContains, startsWith, endsWith, between, notBetween
  - Ejemplo: `where={"id": {"gt": 1}}`
  - Validación unificada de operadores

### Changed
- Refactorización de la validación de operadores
- Unificación de operadores SQL en un solo lugar (validator.py)

### Fixed
- Corrección en la validación de tipos para operadores de comparación
- Simplificación de la clase Table removiendo requerimiento de model_type 