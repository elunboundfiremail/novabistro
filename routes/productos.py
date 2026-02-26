from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_db

router = APIRouter(prefix='/productos', tags=['Productos'])

class Producto(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_bs: float
    id_categoria: int
    disponible: Optional[bool] = True

@router.get('/')
async def listar_productos(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM productos WHERE activo = TRUE')
        productos = await cur.fetchall()
        return productos

@router.post('/')
async def crear_producto(producto: Producto, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''INSERT INTO productos (nombre, descripcion, precio_bs, id_categoria, disponible) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id_producto''',
            (producto.nombre, producto.descripcion, producto.precio_bs, 
             producto.id_categoria, producto.disponible)
        )
        id_producto = await cur.fetchone()
        return {'id_producto': id_producto[0], 'mensaje': 'Producto creado exitosamente'}

@router.put('/{id}')
async def actualizar_producto(id: int, producto: Producto, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''UPDATE productos SET nombre = %s, descripcion = %s, precio_bs = %s, 
               id_categoria = %s, disponible = %s WHERE id_producto = %s''',
            (producto.nombre, producto.descripcion, producto.precio_bs, 
             producto.id_categoria, producto.disponible, id)
        )
        return {'mensaje': 'Producto actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_producto(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE productos SET activo = FALSE WHERE id_producto = %s', (id,))
        return {'mensaje': 'Producto eliminado exitosamente'}
