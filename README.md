# Práctica II - Problema planteado (GET POST PUT DELETE - Flujo completo)

## Introducción
Este repositorio contiene el desarrollo de la **NovaBistro API**, un sistema integral de gestión para restaurantes. En esta fase del proyecto, se han consolidado las operaciones fundamentales de la API, permitiendo un flujo completo de datos a través de los métodos HTTP **GET, POST, PUT y DELETE**.

El sistema permite no solo la creación y lectura de registros, sino también la actualización detallada de la información y la eliminación lógica (soft delete) para mantener la integridad referencial. Además, se ha implementado un módulo de **Reportes** que ofrece una visión general del estado del negocio y detalles individuales por pedido y personal, cumpliendo con los requerimientos de análisis de datos del proyecto.

---

## Estado del Proyecto
**NovaBistro - Sistema de Gestion para Restaurante**

### Características Implementadas
- **CRUD Completo:** Endpoints para Roles, Personal, Mesas, Categorías, Productos y Pedidos.
- **Flujo de Pedidos:** Registro dinámico con cálculo automático de totales basado en productos.
- **Sistema de Reportes:** 
  - Reporte general de ventas y estadísticas.
  - Reporte individual de pedidos con detalle de productos.
  - Reporte de desempeño por personal.
- **Persistencia:** Base de datos PostgreSQL con eliminaciones lógicas.

## Estructura de Endpoints Principales

### Reportes (`/reportes`)
- `GET /reportes/general` - Estadísticas globales de ventas y productos top.
- `GET /reportes/individual/pedido/{id}` - Detalle completo de un pedido específico.
- `GET /reportes/individual/personal/{id}` - Historial y ventas generadas por un empleado.

### Gestión General (PUT/DELETE)
Todos los módulos (`/productos`, `/categorias`, `/mesas`, `/personal`, `/roles`, `/pedidos`) cuentan ahora con:
- `PUT /{id}` - Actualización completa del recurso.
- `DELETE /{id}` - Eliminación lógica (cambio de estado a inactivo).

## Instalación y Ejecución

1. **Sincronizar dependencias:**
   ```bash
   uv sync
   ```

2. **Ejecutar servidor:**
   ```bash
   uv run uvicorn main:app --reload
   ```

3. **Documentación interactiva:**
   Visite `http://127.0.0.1:8000/docs` para probar todos los endpoints implementados.

---
**Autor:** JONATHAN ZUBIETA
**Materia:** Tecnologías Web I
**Fecha:** Marzo 2026
