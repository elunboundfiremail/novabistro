# 📱 Manual de Uso - Thunder Client

## 🔧 Instalación de Thunder Client

1. Abre **VSCode**
2. Ve a **Extensions** (Ctrl+Shift+X)
3. Busca **"Thunder Client"**
4. Click en **Install**

---

## 🚀 Configuración Inicial

### Paso 1: Asegúrate que el servidor esté corriendo

```bash
cd ~/proyecto/novabistro
source venv/bin/activate
uvicorn main:app --reload
```

Verás: `INFO: Uvicorn running on http://127.0.0.1:8000`

### Paso 2: Abrir Thunder Client

- Click en el icono de **rayo** ⚡ en la barra lateral de VSCode
- O presiona: `Ctrl+Shift+R`

---

## 📚 Guía de Uso por Método HTTP

### 🟢 GET - Obtener Datos

#### Ejemplo 1: Listar todas las categorías

1. Click en **"New Request"**
2. Selecciona método: **GET**
3. URL: `http://127.0.0.1:8000/categorias/`
4. Click en **"Send"**

**Respuesta esperada:**
```json
[
  [1, "Entradas", "Platos de entrada", true],
  [2, "Platos principales", "Platos fuertes del menu", true],
  [3, "Bebidas", "Bebidas frias y calientes", true],
  [4, "Postres", "Postres y dulces", true],
  [5, "Sopas", "Sopas tradicionales", true]
]
```

#### Ejemplo 2: Listar todos los productos

- **Método**: GET
- **URL**: `http://127.0.0.1:8000/productos/`

#### Ejemplo 3: Obtener pedidos por estado

- **Método**: GET
- **URL**: `http://127.0.0.1:8000/pedidos/estado/pendiente`

#### Ejemplo 4: Ver detalle de un pedido específico

- **Método**: GET
- **URL**: `http://127.0.0.1:8000/pedidos/detalle/1`

---

### 🟡 POST - Crear Datos

#### Ejemplo 1: Crear una categoría

1. Click en **"New Request"**
2. Método: **POST**
3. URL: `http://127.0.0.1:8000/categorias/`
4. Ve a la pestaña **"Body"**
5. Selecciona **"JSON"**
6. Pega este código:

```json
{
  "nombre": "Ensaladas",
  "descripcion": "Ensaladas frescas y saludables"
}
```

7. Click en **"Send"**

**Respuesta esperada:**
```json
{
  "id_categoria": 6,
  "mensaje": "Categoria creada exitosamente"
}
```

#### Ejemplo 2: Crear un producto

- **Método**: POST
- **URL**: `http://127.0.0.1:8000/productos/`
- **Body (JSON)**:

```json
{
  "nombre": "Silpancho",
  "descripcion": "Plato típico cochabambino",
  "precio_bs": 35.00,
  "id_categoria": 2,
  "disponible": true
}
```

⚠️ **Importante**: El `id_categoria` debe existir. Primero haz GET /categorias/ para ver los IDs disponibles.

#### Ejemplo 3: Crear un rol

- **Método**: POST
- **URL**: `http://127.0.0.1:8000/roles/`
- **Body (JSON)**:

```json
{
  "nombre": "Chef",
  "descripcion": "Chef principal de cocina"
}
```

#### Ejemplo 4: Crear una mesa

- **Método**: POST
- **URL**: `http://127.0.0.1:8000/mesas/`
- **Body (JSON)**:

```json
{
  "numero": 10,
  "capacidad": 4,
  "ubicacion": "Salón VIP",
  "estado": "disponible"
}
```

#### Ejemplo 5: Crear personal

- **Método**: POST
- **URL**: `http://127.0.0.1:8000/personal/`
- **Body (JSON)**:

```json
{
  "ci": "12345678",
  "nombre": "Juan",
  "apellido_paterno": "Pérez",
  "apellido_materno": "López",
  "fecha_nacimiento": "1990-05-15",
  "direccion": "Av. Principal #123",
  "telefono": "77777777",
  "email": "juan.perez@novabistro.com",
  "id_rol": 2
}
```

⚠️ **Importante**: El `id_rol` debe existir.

#### Ejemplo 6: Crear un pedido completo (con detalles)

- **Método**: POST
- **URL**: `http://127.0.0.1:8000/pedidos/`
- **Body (JSON)**:

```json
{
  "numero_pedido": "PED-001",
  "id_mesa": 1,
  "id_personal": 1,
  "estado": "pendiente",
  "observaciones": "Cliente sin cebolla",
  "detalles": [
    {
      "id_producto": 1,
      "cantidad": 2,
      "observaciones": "Bien cocido"
    },
    {
      "id_producto": 2,
      "cantidad": 1,
      "observaciones": null
    }
  ]
}
```

**Nota**: El `total_bs` se calcula automáticamente basado en los precios de los productos.

---

### 🔵 PUT - Actualizar Datos

#### Ejemplo 1: Actualizar una categoría

- **Método**: PUT
- **URL**: `http://127.0.0.1:8000/categorias/1`
- **Body (JSON)**:

```json
{
  "nombre": "Entradas Gourmet",
  "descripcion": "Entradas especiales de la casa"
}
```

#### Ejemplo 2: Actualizar un producto

- **Método**: PUT
- **URL**: `http://127.0.0.1:8000/productos/1`
- **Body (JSON)**:

```json
{
  "nombre": "Pique Macho Especial",
  "descripcion": "Plato típico boliviano con carne premium",
  "precio_bs": 55.00,
  "id_categoria": 2,
  "disponible": true
}
```

#### Ejemplo 3: Actualizar un pedido

- **Método**: PUT
- **URL**: `http://127.0.0.1:8000/pedidos/1`
- **Body (JSON)**:

```json
{
  "numero_pedido": "PED-001-MOD",
  "id_mesa": 2,
  "id_personal": 1,
  "estado": "en_proceso",
  "observaciones": "Cliente pidió cambio de mesa"
}
```

---

### 🟠 PATCH - Actualización Parcial

#### Ejemplo: Cambiar estado de un pedido

- **Método**: PATCH
- **URL**: `http://127.0.0.1:8000/pedidos/1/estado?estado=completado`

**Estados válidos**: 
- `pendiente`
- `en_proceso`
- `completado`
- `entregado`
- `cancelado`

---

### 🔴 DELETE - Eliminar Datos (Soft Delete)

#### Ejemplo 1: Eliminar una categoría

- **Método**: DELETE
- **URL**: `http://127.0.0.1:8000/categorias/6`

**Nota**: Es un "soft delete", solo marca como `activo = false`, no borra físicamente.

#### Ejemplo 2: Eliminar un producto

- **Método**: DELETE
- **URL**: `http://127.0.0.1:8000/productos/1`

#### Ejemplo 3: Eliminar un pedido

- **Método**: DELETE
- **URL**: `http://127.0.0.1:8000/pedidos/1`

---

## 💾 Guardar Requests (Colecciones)

### Crear una colección:

1. En Thunder Client, click en **"Collections"**
2. Click en **"+"** para crear nueva colección
3. Nombra: "NovaBistro API"
4. Guarda cada request en esta colección

### Guardar un request:

1. Después de crear un request
2. Click en **"Save"**
3. Selecciona la colección "NovaBistro API"
4. Dale un nombre descriptivo (ej: "POST Crear Producto")

---

## 🎯 Flujo de Trabajo Recomendado

### Para crear un producto nuevo:

```
1. GET /categorias/          → Ver qué categorías existen
2. POST /categorias/         → (Opcional) Crear nueva categoría
3. POST /productos/          → Crear producto usando id_categoria válido
4. GET /productos/           → Verificar que se creó
```

### Para crear un pedido:

```
1. GET /mesas/               → Ver mesas disponibles
2. GET /personal/            → Ver personal disponible
3. GET /productos/           → Ver productos disponibles
4. POST /pedidos/            → Crear pedido con detalles
5. GET /pedidos/detalle/{id} → Verificar el pedido completo
```

---

## 🐛 Solución de Errores Comunes

### Error 307 - Temporary Redirect
**Problema**: Falta la barra `/` al final de la URL
- ❌ `http://127.0.0.1:8000/productos`
- ✅ `http://127.0.0.1:8000/productos/`

### Error 422 - Unprocessable Entity
**Problema**: Falta un campo requerido o tipo de dato incorrecto
- Verifica que todos los campos requeridos estén presentes
- Verifica que los tipos de datos sean correctos (números, strings, etc.)

### Error 404 - Not Found
**Problema**: La URL o el ID no existe
- Verifica la URL
- Si es un PUT/DELETE, verifica que el ID exista

### Error: Foreign Key Constraint
**Problema**: Intentas usar un ID que no existe
- Ejemplo: `id_categoria: 999` cuando solo existen 1-5
- Solución: Haz GET primero para ver los IDs disponibles

### Error: Connection Refused
**Problema**: El servidor no está corriendo
- Solución: `uvicorn main:app --reload`

---

## 📊 Estructura de Respuestas

### GET - Lista de datos
```json
[
  [1, "Nombre", "Descripción", true],
  [2, "Nombre2", "Descripción2", true]
]
```

### POST - Creación exitosa
```json
{
  "id_categoria": 1,
  "mensaje": "Categoria creada exitosamente"
}
```

### PUT/PATCH - Actualización exitosa
```json
{
  "mensaje": "Categoria actualizada exitosamente"
}
```

### DELETE - Eliminación exitosa
```json
{
  "mensaje": "Categoria eliminada exitosamente"
}
```

---

## 🎓 Tips y Buenas Prácticas

1. **Siempre usa la barra `/` al final** de las URLs
2. **Haz GET antes de POST** para ver qué IDs existen
3. **Guarda tus requests** en colecciones para reutilizarlos
4. **Usa nombres descriptivos** para tus requests guardados
5. **Verifica con GET** después de cada POST/PUT/DELETE
6. **Revisa los logs del servidor** si algo falla

---

## 📝 Endpoints Disponibles

### Categorías
- `GET /categorias/` - Listar
- `POST /categorias/` - Crear
- `PUT /categorias/{id}` - Actualizar
- `DELETE /categorias/{id}` - Eliminar

### Productos
- `GET /productos/` - Listar
- `POST /productos/` - Crear
- `PUT /productos/{id}` - Actualizar
- `DELETE /productos/{id}` - Eliminar

### Pedidos
- `GET /pedidos/` - Listar
- `GET /pedidos/estado/{estado}` - Filtrar
- `GET /pedidos/detalle/{id}` - Detalle completo
- `POST /pedidos/` - Crear
- `PATCH /pedidos/{id}/estado` - Cambiar estado
- `PUT /pedidos/{id}` - Actualizar
- `DELETE /pedidos/{id}` - Eliminar

### Roles
- `GET /roles/` - Listar
- `POST /roles/` - Crear
- `PUT /roles/{id}` - Actualizar
- `DELETE /roles/{id}` - Eliminar

### Personal
- `GET /personal/` - Listar
- `POST /personal/` - Crear
- `PUT /personal/{id}` - Actualizar
- `DELETE /personal/{id}` - Eliminar

### Mesas
- `GET /mesas/` - Listar
- `POST /mesas/` - Crear
- `PUT /mesas/{id}` - Actualizar
- `DELETE /mesas/{id}` - Eliminar

---

✅ **Con esta guía podrás usar Thunder Client para probar todos los endpoints de tu API**
