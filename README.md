# NovaBistro - Sistema Integral de Gestión Gastronómica (Fase Beta)

## Introducción
**NovaBistro** es una solución tecnológica robusta diseñada para la digitalización y optimización de procesos operativos en el sector gastronómico. Este sistema centraliza la gestión de ventas, inventario de productos, administración de personal y análisis de datos en tiempo real, proporcionando una herramienta escalable para la toma de decisiones estratégicas.

En su actual **fase beta**, el sistema ha completado la integración de todos sus módulos críticos, garantizando la persistencia de datos mediante una arquitectura de microservicios ligera y una interfaz de usuario reactiva y profesional.

---

## Características Principales del Ecosistema

### 1. Motor de Ventas y Pedidos
- **Gestión Atómica:** Procesamiento de órdenes multi-producto con validación de integridad.
- **Cálculos Dinámicos:** Eliminación de redundancia de datos mediante el cálculo de subtotales y totales en tiempo real a través del motor SQL.
- **Control de Salón:** Visualización interactiva del estado de mesas (Disponible/Ocupada).

### 2. Dashboard Administrativo (Control Total)
- **Gestión de Personal:** Registro y control de acceso basado en roles (Admin, Mesero, Cocina, Caja).
- **Catálogo Inteligente:** Administración dinámica de categorías y productos con soporte para descripciones detalladas.
- **Borrado Lógico (Soft Delete):** Implementación de seguridad de datos donde los registros no se eliminan físicamente, manteniendo la integridad histórica para auditorías.

### 3. Módulo de Inteligencia de Negocios (Reportes)
- **Reporte General:** Análisis de ventas brutas, pedidos finalizados y rendimiento por categoría.
- **Auditoría Individual:** Seguimiento detallado del desempeño por empleado y trazabilidad de cada pedido.
- **Reporte Diario:** Control de flujo de caja y ventas del día en curso.

---

## Arquitectura Técnica
- **Backend:** FastAPI (Python 3.12+) - Alto rendimiento y documentación automática.
- **Base de Datos:** PostgreSQL - Relaciones sólidas y procedimientos optimizados.
- **Frontend:** HTML5, Tailwind CSS y JavaScript Vanilla - Interfaz rápida, sin dependencias pesadas y optimizada para terminales de punto de venta.
- **Seguridad:** Encriptación de credenciales mediante `bcrypt` y validación de estado activo para todos los usuarios.

---

## Guía de Despliegue Rápido

### Requisitos Previos
- Python 3.12+
- PostgreSQL 15+
- Gestor de paquetes `uv` (recomendado) o `pip`.

### Instalación
1. **Clonar el repositorio y acceder a la carpeta:**
   ```bash
   git clone <url-repositorio>
   cd novabistro
   ```

2. **Sincronizar el entorno virtual y dependencias:**
   ```bash
   uv sync
   ```

3. **Configurar la Base de Datos:**
   Importar el archivo `base_datos/novabistro.sql` en su instancia de PostgreSQL.

4. **Iniciar el Ecosistema:**
   ```bash
   uv run uvicorn main:app --reload
   ```

5. **Acceso al Sistema:**
   - **Frontend:** Abrir `front/index.html` en el navegador.
   - **API Docs (Swagger):** `http://127.0.0.1:8000/docs`

---
**Desarrollado por:** Jonathan Zubieta  
**Versión:** 1.0.0-beta  
**Estado:** Estable / Pruebas de Integración Completadas  
**Localización:** Santa Cruz - Bolivia (2026)
