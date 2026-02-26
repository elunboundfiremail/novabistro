from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_db

router = APIRouter(prefix='/roles', tags=['Roles'])

class Rol(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

@router.get('/')
async def listar_roles(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM roles WHERE activo = TRUE')
        roles = await cur.fetchall()
        return roles

@router.post('/')
async def crear_rol(rol: Rol, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'INSERT INTO roles (nombre, descripcion) VALUES (%s, %s) RETURNING id_rol',
            (rol.nombre, rol.descripcion)
        )
        id_rol = await cur.fetchone()
        return {'id_rol': id_rol[0], 'mensaje': 'Rol creado exitosamente'}

@router.put('/{id}')
async def actualizar_rol(id: int, rol: Rol, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'UPDATE roles SET nombre = %s, descripcion = %s WHERE id_rol = %s',
            (rol.nombre, rol.descripcion, id)
        )
        return {'mensaje': 'Rol actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_rol(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE roles SET activo = FALSE WHERE id_rol = %s', (id,))
        return {'mensaje': 'Rol eliminado exitosamente'}
