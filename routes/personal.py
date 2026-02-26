from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from config.conexionDB import get_db

router = APIRouter(prefix='/personal', tags=['Personal'])

class Personal(BaseModel):
    ci: str
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    id_rol: int

@router.get('/')
async def listar_personal(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM personal WHERE activo = TRUE')
        personal = await cur.fetchall()
        return personal

@router.post('/')
async def crear_personal(persona: Personal, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''INSERT INTO personal (ci, nombre, apellido_paterno, apellido_materno, 
               fecha_nacimiento, direccion, telefono, email, id_rol) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_personal''',
            (persona.ci, persona.nombre, persona.apellido_paterno, persona.apellido_materno,
             persona.fecha_nacimiento, persona.direccion, persona.telefono, persona.email, persona.id_rol)
        )
        id_personal = await cur.fetchone()
        return {'id_personal': id_personal[0], 'mensaje': 'Personal creado exitosamente'}

@router.put('/{id}')
async def actualizar_personal(id: int, persona: Personal, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''UPDATE personal SET ci = %s, nombre = %s, apellido_paterno = %s, 
               apellido_materno = %s, fecha_nacimiento = %s, direccion = %s, 
               telefono = %s, email = %s, id_rol = %s WHERE id_personal = %s''',
            (persona.ci, persona.nombre, persona.apellido_paterno, persona.apellido_materno,
             persona.fecha_nacimiento, persona.direccion, persona.telefono, persona.email, 
             persona.id_rol, id)
        )
        return {'mensaje': 'Personal actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_personal(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE personal SET activo = FALSE WHERE id_personal = %s', (id,))
        return {'mensaje': 'Personal eliminado exitosamente'}
