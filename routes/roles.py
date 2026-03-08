from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_db
from psycopg.rows import dict_row

router = APIRouter(prefix='/roles', tags=['Roles'])

class Rol(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

@router.get('/')
async def listar_roles(conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('SELECT * FROM roles WHERE activo = TRUE')
        roles = await cur.fetchall()
        return roles

@router.post('/')
async def crear_rol(rol: Rol, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            'INSERT INTO roles (nombre, descripcion) VALUES (%s, %s) RETURNING id_rol',
            (rol.nombre, rol.descripcion)
        )
        id_rol = await cur.fetchone()
        return {'id_rol': id_rol['id_rol'], 'mensaje': 'Rol creado exitosamente'}

@router.delete('/{id}')
async def eliminar_rol(id: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('UPDATE roles SET activo = FALSE WHERE id_rol = %s', (id,))
        return {'mensaje': 'Rol eliminado exitosamente'}
