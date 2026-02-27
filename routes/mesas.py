from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from config.conexionDB import get_db

router = APIRouter(prefix='/mesas', tags=['Mesas'])

class Mesa(BaseModel):
    numero: int
    capacidad: int
    ubicacion: Optional[str] = None
    estado: Optional[str] = 'disponible'

@router.get('/')
async def listar_mesas(conn = Depends(get_db)):
    print("listando pedidos")
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM mesas WHERE activo = TRUE')
        mesas = await cur.fetchall()
        return mesas

@router.post('/')
async def crear_mesa(mesa: Mesa, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'INSERT INTO mesas (numero, capacidad, ubicacion, estado) VALUES (%s, %s, %s, %s) RETURNING id_mesa',
            (mesa.numero, mesa.capacidad, mesa.ubicacion, mesa.estado)
        )
        id_mesa = await cur.fetchone()
        return {'id_mesa': id_mesa[0], 'mensaje': 'Mesa creada exitosamente'}

@router.put('/{id}')
async def actualizar_mesa(id: int, mesa: Mesa, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            'UPDATE mesas SET numero = %s, capacidad = %s, ubicacion = %s, estado = %s WHERE id_mesa = %s',
            (mesa.numero, mesa.capacidad, mesa.ubicacion, mesa.estado, id)
        )
        return {'mensaje': 'Mesa actualizada exitosamente'}

@router.delete('/{id}')
async def eliminar_mesa(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE mesas SET activo = FALSE WHERE id_mesa = %s', (id,))
        return {'mensaje': 'Mesa eliminada exitosamente'}
