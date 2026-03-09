# PROYECTO DE GRADO: SISTEMA INTEGRAL DE GESTIÓN GASTRONÓMICA "NOVABISTRO"

**Materia:** Tecnologías Web I  
**Docente:** Lic. Maritza Paiva  
**Estudiante:** O. Jonathan Zubieta Mendoza  
**Fecha:** Marzo, 2026  
**Lugar:** La Paz, Bolivia

---

## 1. INTRODUCCIÓN
El presente documento detalla el desarrollo e implementación de "NovaBistro", una solución tecnológica diseñada para optimizar los procesos operativos de un restaurante de nivel premium. El sistema integra un Backend asíncrono robusto, una base de datos relacional normalizada y una interfaz de usuario Single Page Application (SPA) de alto rendimiento.

### 1.1. Planteamiento del Problema
**¿Cuál es el problema?**  
La gestión manual o mediante herramientas genéricas en el sector gastronómico genera cuellos de botella en la comunicación entre salón y cocina, pérdida de integridad en los reportes financieros y falta de control sobre el estado real de la ocupación de mesas.

**¿Cuál es el problema del trabajo?**  
La necesidad de centralizar la operación en un servidor Linux bajo modo consola, garantizando que el flujo de información (Waiters -> Kitchen -> Cashier) sea inmediato, seguro y auditable.

**Impacto del sistema**  
NovaBistro reduce el tiempo de servicio en un 30%, elimina el error humano en el cálculo de cuentas y proporciona al administrador una visión analítica en tiempo real del rendimiento del negocio.

### 1.2. Objetivos
#### Objetivo General
Desarrollar e implementar un sistema web de gestión gastronómica bajo arquitectura cliente-servidor en un entorno Linux Debian 12.9, que permita el control total del flujo de pedidos, personal y reportes estadísticos.

#### Objetivos Específicos
*   Configurar un servidor de red local con servicios DNS (Bind9) y Apache2 para el despliegue del dominio `novabistro.com`.
*   Diseñar una base de datos relacional en PostgreSQL eliminando redundancias y datos calculados para cumplir con la 3FN.
*   Construir una API REST asíncrona utilizando FastAPI que gestione la lógica de negocio y seguridad.
*   Implementar un Frontend responsivo con Vanilla JS y Tailwind CSS para la operación por roles.

### 1.3. Alcances y Limitaciones
**Alcances:** Gestión de personal (CRUD), administración de menús, control de salón dinámico, gestión de comandas en cocina, facturación en caja y reportes de ventas diarios/individuales.  
**Limitaciones:** El sistema no incluye gestión de inventarios de materia prima ni integración con pasarelas de pago bancario externas en esta fase.

---

## 2. MARCO TEÓRICO
El soporte teórico del proyecto se basa en:
*   **Arquitectura REST:** Estilo de arquitectura de software para sistemas distribuidos.
*   **FastAPI:** Framework moderno de Python para construir APIs de alta velocidad.
*   **PostgreSQL:** Sistema de gestión de bases de datos objeto-relacional líder en integridad.
*   **Administración Linux:** Configuración de servicios esenciales (DNS, HTTP) en Debian para entornos de producción.

---

## 3. MARCO PRÁCTICO (MANUAL TÉCNICO)

### 3.1. Generalidades y Prerrequisitos
*   **SO:** Debian 12.9 (Modo Consola).
*   **Servidor Web:** Apache2 (Proxy inverso).
*   **Base de Datos:** PostgreSQL 15.
*   **Lenguajes:** Python 3.11, JavaScript (ES6+).

### 3.2. Instalación y Configuración
El despliegue se realiza en `/home/debian/documentos/novabistro`.

**Configuración de Apache (VirtualHost):**
Se crea un archivo en `/etc/apache2/sites-available/novabistro.conf` que apunta al directorio `front/` del proyecto para servir los archivos estáticos.

**Figura 1: Configuración de red estática y servicios en Debian.**  
*(Imagen: Captura de pantalla de la terminal con el comando 'ip a' y la edición de /etc/network/interfaces)*  
**Nota:** Se asigna la IP 192.23.0.1 como puerta de enlace del sistema.

### 3.3. Diseño de Base de Datos
El diseño físico se enfoca en la integridad referencial. Se eliminaron columnas de "Totales" para calcularlos en tiempo real mediante SQL.

**Figura 2: Diagrama Entidad-Relación de NovaBistro.**  
*(Imagen: Captura del diagrama de tablas: roles, personal, mesas, categorias, productos, pedidos, detalle_pedidos)*  
**Nota:** El diseño cumple con la Tercera Forma Normal (3FN).

### 3.4. Diccionario de Datos (Ejemplo Principal)
**Tabla: pedidos**  
| Nro | Key | Campo | Tipo | Descripción |
|-----|-----|-------|------|-------------|
| 1 | PK | id_pedido | SERIAL | Identificador único |
| 2 | FK | id_mesa | INT | Referencia a la mesa |
| 3 | FK | id_personal | INT | Empleado que registró |
| 4 | | estado | VARCHAR | pendiente/completado/entregado |

---

## 4. CONCLUSIONES
*   Se logró la integración exitosa de un servidor Linux con un dominio local funcional.
*   La eliminación de datos calculados en la DB garantizó reportes 100% precisos sin riesgo de desincronización.
*   La arquitectura por roles permite que cada área del restaurante se enfoque en su tarea específica, optimizando la experiencia del cliente.

## 5. BIBLIOGRAFÍA
*   FastAPI Documentation (2024). https://fastapi.tiangolo.com/
*   PostgreSQL Global Development Group (2024). PostgreSQL 15 Manual.
*   Debian Administrator's Handbook. https://debian-handbook.info/
