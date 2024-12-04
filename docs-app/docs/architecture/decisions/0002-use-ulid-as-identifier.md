# 2. Usar ULID como Identificador

Fecha: 2023-11-15

## Estado

Aceptado

## Contexto

Necesitamos un sistema de identificadores únicos para nuestras entidades que sea:
- Globalmente único
- Ordenable temporalmente
- Seguro para URLs
- Eficiente en bases de datos

## Decisión

Usaremos ULID (Universally Unique Lexicographically Sortable Identifier) en lugar de UUID por las siguientes ventajas:

1. **Ordenación Temporal**: Los ULID están ordenados lexicográficamente y contienen un timestamp, lo que facilita:
   - Ordenación natural por fecha de creación
   - Indexación más eficiente en bases de datos
   - Mejor rendimiento en consultas por rango

2. **Formato Amigable**:
   - 26 caracteres en Base32 (vs 36 caracteres del UUID)
   - Seguros para URLs sin necesidad de encoding
   - Más legibles que los UUID

3. **Compatibilidad**:
   - Mantiene la unicidad global como UUID
   - Compatible con sistemas existentes
   - Fácil de integrar con diferentes bases de datos

## Implementación

Usaremos la biblioteca `python-ulid` que proporciona:
- Generación thread-safe de ULIDs
- Serialización/deserialización
- Compatibilidad con UUID cuando sea necesario

Ejemplo de ULID:
```python
01ARZ3NDEKTSV4RRFFQ69G5FAV
```

Donde:
- Los primeros 10 caracteres son el timestamp en milisegundos
- Los siguientes 16 caracteres son aleatorios

## Consecuencias

### Positivas
- Mejor rendimiento en consultas de base de datos
- IDs ordenables temporalmente
- Más cortos y legibles que UUID
- No requieren índices adicionales para ordenación temporal

### Negativas
- Menos soporte nativo en algunas bases de datos
- Requiere biblioteca adicional
- Posible necesidad de migración de datos existentes
