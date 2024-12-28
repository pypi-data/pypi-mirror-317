# Changelog

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