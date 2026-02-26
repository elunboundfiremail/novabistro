from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_db

router = APIRouter(prefix='/categorias', tags=['Categorias'])

class Categoria(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

@router.get('/')
async def listar_categorias(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM categorias WHERE activo = TRUE')
        categorias = await cur.fetchall()
        return categorias

@router.post('/')
async def crear_categoria(categoria: Categoria, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id_categoria',
            (categoria.nombre, categoria.descripcion)
        )
        id_categoria = await cur.fetchone()
        return {'id_categoria': id_categoria[0], 'mensaje': 'Categoria creada exitosamente'}

@router.put('/{id}')
async def actualizar_categoria(id: int, categoria: Categoria, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'UPDATE categorias SET nombre = %s, descripcion = %s WHERE id_categoria = %s',
            (categoria.nombre, categoria.descripcion, id)
        )
        return {'mensaje': 'Categoria actualizada exitosamente'}

@router.delete('/{id}')
async def eliminar_categoria(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE categorias SET activo = FALSE WHERE id_categoria = %s', (id,))
        return {'mensaje': 'Categoria eliminada exitosamente'}
