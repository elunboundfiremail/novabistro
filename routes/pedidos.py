from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from config.conexionDB import get_db

router = APIRouter(prefix='/pedidos', tags=['Pedidos'])

class Pedido(BaseModel):
    numero_pedido: str
    id_mesa: int
    id_personal: int
    estado: Optional[str] = 'pendiente'
    total_bs: Optional[float] = 0.00
    observaciones: Optional[str] = None

@router.get('/')
async def listar_pedidos(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM pedidos WHERE activo = TRUE ORDER BY fecha_pedido DESC')
        pedidos = await cur.fetchall()
        return pedidos

@router.get('/estado/{estado}')
async def listar_pedidos_por_estado(estado: str, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT * FROM pedidos WHERE estado = %s AND activo = TRUE', (estado,))
        pedidos = await cur.fetchall()
        return pedidos

@router.post('/')
async def crear_pedido(pedido: Pedido, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''INSERT INTO pedidos (numero_pedido, id_mesa, id_personal, estado, total_bs, observaciones) 
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pedido''',
            (pedido.numero_pedido, pedido.id_mesa, pedido.id_personal, 
             pedido.estado, pedido.total_bs, pedido.observaciones)
        )
        id_pedido = await cur.fetchone()
        return {'id_pedido': id_pedido[0], 'mensaje': 'Pedido creado exitosamente'}

@router.put('/{id}')
async def actualizar_pedido(id: int, pedido: Pedido, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''UPDATE pedidos SET numero_pedido = %s, id_mesa = %s, id_personal = %s, 
               estado = %s, total_bs = %s, observaciones = %s WHERE id_pedido = %s''',
            (pedido.numero_pedido, pedido.id_mesa, pedido.id_personal, 
             pedido.estado, pedido.total_bs, pedido.observaciones, id)
        )
        return {'mensaje': 'Pedido actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_pedido(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE pedidos SET activo = FALSE WHERE id_pedido = %s', (id,))
        return {'mensaje': 'Pedido eliminado exitosamente'}
