# Changelog

## [0.1.24] - 2024-03-19

### Added
- Agregados métodos `query()` y `execute()` en PrismaLikeClient para ejecutar SQL raw directamente
- El método `query()` permite ejecutar SELECT y retorna los resultados como lista de diccionarios
- El método `execute()` permite ejecutar INSERT/UPDATE/DELETE sin retorno de resultados

### Fixed
- Corregido el manejo de stubs y autocompletado 