# NovaBistro - Sistema de Gestion para Restaurante

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.132.0-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)

## Descripcion

NovaBistro es un sistema de gestion integral para restaurantes desarrollado con tecnologias web modernas. Permite la administracion de pedidos, mesas, personal, productos y categorias mediante una API REST robusta y escalable.

El sistema esta diseñado especificamente para el contexto boliviano, utilizando terminologia apropiada (CI, Bolivianos) y sin tildes para garantizar compatibilidad de sistemas.

## Estado del Proyecto

**Etapa Actual: Fase 1 - API REST Completa**

- [x] Base de datos diseñada e implementada (7 tablas)
- [x] API REST con 31 endpoints funcionales
- [x] Pruebas de endpoints exitosas (100%)
- [x] Documentacion completa
- [ ] Fase 2 - Frontend (Proximamente)
- [ ] Fase 3 - Autenticacion y autorizacion
- [ ] Fase 4 - Notificaciones en tiempo real

## Caracteristicas

- Gestion de roles y personal
- Control de mesas y ubicaciones
- Administracion de productos y categorias
- Sistema completo de pedidos
- Actualizaciones en tiempo real
- Soft delete (eliminacion logica)
- Base de datos optimizada con indices

## Tecnologias Utilizadas

- **Backend:** FastAPI 0.132.0
- **Base de Datos:** PostgreSQL 12+
- **ORM/Driver:** psycopg 3.3.3
- **Validacion:** Pydantic 2.12.5
- **Servidor:** Uvicorn 0.41.0
- **Gestor de Paquetes:** UV
- **Lenguaje:** Python 3.10+

## Estructura del Proyecto

```
novabistro/
├── base_datos/
│   └── schema.sql              # Script de creacion de BD
├── config/
│   └── conexionDB.py          # Configuracion de PostgreSQL
├── routes/
│   ├── roles.py               # CRUD de roles
│   ├── personal.py            # CRUD de personal
│   ├── mesas.py               # CRUD de mesas
│   ├── categorias.py          # CRUD de categorias
│   ├── productos.py           # CRUD de productos
│   └── pedidos.py             # CRUD de pedidos
├── documentacion/
│   └── DOCUMENTO_PROYECTO_NOVABISTRO.txt
├── main.py                    # Aplicacion principal
├── pyproject.toml             # Dependencias
├── .gitignore
└── README.md
```

## Instalacion

### Requisitos Previos

- Python 3.10 o superior
- PostgreSQL 12 o superior
- UV (gestor de paquetes)

### Instalacion de UV

**Windows (PowerShell):**
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuracion del Proyecto

1. **Clonar el repositorio:**
```bash
git clone https://github.com/elunboundfiremail/novabistro.git
cd novabistro
```

2. **Crear la base de datos:**
```bash
psql -U postgres
CREATE DATABASE novabistro;
\q
```

3. **Ejecutar el script SQL:**
```bash
psql -U postgres -d novabistro -f base_datos/schema.sql
```

4. **Configurar variables de entorno:**

Editar `config/conexionDB.py` si es necesario (por defecto usa `postgres:12345678@localhost:5432/novabistro`)

5. **Instalar dependencias:**
```bash
uv sync
```

6. **Ejecutar la aplicacion:**
```bash
uv run uvicorn main:app --reload
```

7. **Acceder a la API:**
- API: http://127.0.0.1:8000
- Documentacion Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Documentacion de API

### Endpoints Disponibles (31 total)

#### Roles (`/roles`)
- `GET /roles` - Listar todos los roles
- `POST /roles` - Crear nuevo rol
- `PUT /roles/{id}` - Actualizar rol
- `DELETE /roles/{id}` - Eliminar rol (soft delete)

#### Personal (`/personal`)
- `GET /personal` - Listar todo el personal
- `POST /personal` - Registrar nuevo personal
- `PUT /personal/{id}` - Actualizar personal
- `DELETE /personal/{id}` - Dar de baja personal

#### Mesas (`/mesas`)
- `GET /mesas` - Listar todas las mesas
- `POST /mesas` - Crear nueva mesa
- `PUT /mesas/{id}` - Actualizar mesa
- `DELETE /mesas/{id}` - Eliminar mesa

#### Categorias (`/categorias`)
- `GET /categorias` - Listar categorias
- `POST /categorias` - Crear categoria
- `PUT /categorias/{id}` - Actualizar categoria
- `DELETE /categorias/{id}` - Eliminar categoria

#### Productos (`/productos`)
- `GET /productos` - Listar productos
- `POST /productos` - Crear producto
- `PUT /productos/{id}` - Actualizar producto
- `DELETE /productos/{id}` - Eliminar producto

#### Pedidos (`/pedidos`)
- `GET /pedidos` - Listar pedidos
- `GET /pedidos/estado/{estado}` - Filtrar por estado
- `POST /pedidos` - Crear pedido
- `PUT /pedidos/{id}` - Actualizar pedido
- `DELETE /pedidos/{id}` - Cancelar pedido

### Ejemplos de Uso

**Crear una categoria:**
```bash
curl -X POST "http://127.0.0.1:8000/categorias" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Platos principales",
    "descripcion": "Platos fuertes del menu"
  }'
```

**Crear un producto:**
```bash
curl -X POST "http://127.0.0.1:8000/productos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pique macho",
    "descripcion": "Plato tipico boliviano",
    "precio_bs": 45.50,
    "id_categoria": 2,
    "disponible": true
  }'
```

**Obtener pedidos pendientes:**
```bash
curl -X GET "http://127.0.0.1:8000/pedidos/estado/pendiente"
```

## Base de Datos

### Tablas

1. **roles** - Roles de usuario (Administrador, Mesero, Cocinero, Cajero)
2. **personal** - Informacion de empleados
3. **mesas** - Mesas del restaurante
4. **categorias** - Categorias de productos
5. **productos** - Productos del menu
6. **pedidos** - Pedidos realizados
7. **detalle_pedidos** - Detalle de productos por pedido

### Diagrama ER

```
ROLES (1) ----< (N) PERSONAL (1) ----< (N) PEDIDOS
                                              |
CATEGORIAS (1) ----< (N) PRODUCTOS           |
                            |                 |
                            +-------> DETALLE_PEDIDOS
                                       
MESAS (1) ----< (N) PEDIDOS
```

## Pruebas

Para probar los endpoints se puede utilizar:

1. **Swagger UI** (recomendado): http://127.0.0.1:8000/docs
2. **ThunderClient** (VS Code)
3. **Postman**
4. **cURL**

Todas las pruebas actuales han sido exitosas (100% de endpoints funcionales).

## Documentacion Adicional

Para documentacion tecnica completa, ver:
- `documentacion/DOCUMENTO_PROYECTO_NOVABISTRO.txt` - Documentacion exhaustiva del proyecto

## Autores

Proyecto academico desarrollado para la materia Tecnologias Web I

- Universidad: [Tu Universidad]
- Fecha: Febrero 2026

## Proximas Funcionalidades

- [ ] Sistema de autenticacion con JWT
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Frontend web responsivo
- [ ] Sistema de reportes y estadisticas
- [ ] Notificaciones push
- [ ] Impresion de comandas
- [ ] Integracion con sistemas de pago
- [ ] App movil para meseros

## Contribuciones

Este es un proyecto academico. Las contribuciones estan cerradas hasta finalizar la evaluacion.

## Contacto

Para consultas sobre el proyecto, contactar a traves del repositorio de GitHub.

---

**NovaBistro** - Sistema de Gestion para Restaurantes
Desarrollado usando Python y FastAPI
