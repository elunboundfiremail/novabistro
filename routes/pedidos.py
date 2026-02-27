from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from config.conexionDB import get_db

router = APIRouter(prefix='/pedidos', tags=['Pedidos'])

class DetallePedido(BaseModel):
    id_producto: int
    cantidad: int
    observaciones: Optional[str] = None

class Pedido(BaseModel):
    numero_pedido: str
    id_mesa: int
    id_personal: int
    estado: Optional[str] = 'pendiente'
    observaciones: Optional[str] = None
    detalles: List[DetallePedido] = []

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

@router.get('/detalle/{id_pedido}')
async def obtener_pedido_con_detalles(id_pedido: int, conn = Depends(get_db)):
    """Obtener un pedido específico con todos sus detalles"""
    async with conn.cursor() as cur:
        # Obtener datos del pedido
        await cur.execute(
            '''SELECT id_pedido, numero_pedido, id_mesa, id_personal, 
                      fecha_pedido, estado, total_bs, observaciones 
               FROM pedidos WHERE id_pedido = %s AND activo = TRUE''',
            (id_pedido,)
        )
        pedido = await cur.fetchone()
        
        if not pedido:
            return {'error': 'Pedido no encontrado'}
        
        # Obtener detalles del pedido
        await cur.execute(
            '''SELECT dp.id_detalle, dp.id_producto, p.nombre AS producto,
                      dp.cantidad, dp.precio_unitario_bs, dp.subtotal_bs, dp.observaciones
               FROM detalle_pedidos dp
               JOIN productos p ON dp.id_producto = p.id_producto
               WHERE dp.id_pedido = %s''',
            (id_pedido,)
        )
        detalles = await cur.fetchall()
        
        return {
            'pedido': {
                'id_pedido': pedido[0],
                'numero_pedido': pedido[1],
                'id_mesa': pedido[2],
                'id_personal': pedido[3],
                'fecha_pedido': str(pedido[4]),
                'estado': pedido[5],
                'total_bs': float(pedido[6]),
                'observaciones': pedido[7]
            },
            'detalles': [
                {
                    'id_detalle': d[0],
                    'id_producto': d[1],
                    'producto': d[2],
                    'cantidad': d[3],
                    'precio_unitario_bs': float(d[4]),
                    'subtotal_bs': float(d[5]),
                    'observaciones': d[6]
                }
                for d in detalles
            ]
        }

@router.post('/')
async def crear_pedido(pedido: Pedido, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        # Calcular el total del pedido
        total_bs = 0.00
        detalles_con_precios = []
        
        # Obtener precio de cada producto y calcular subtotales
        for detalle in pedido.detalles:
            await cur.execute(
                'SELECT precio_bs FROM productos WHERE id_producto = %s AND activo = TRUE',
                (detalle.id_producto,)
            )
            resultado = await cur.fetchone()
            if resultado:
                precio_unitario = float(resultado[0])
                subtotal = precio_unitario * detalle.cantidad
                total_bs += subtotal
                detalles_con_precios.append({
                    'id_producto': detalle.id_producto,
                    'cantidad': detalle.cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'observaciones': detalle.observaciones
                })
        
        # Insertar el pedido principal
        await cur.execute(
            '''INSERT INTO pedidos (numero_pedido, id_mesa, id_personal, estado, total_bs, observaciones) 
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_pedido''',
            (pedido.numero_pedido, pedido.id_mesa, pedido.id_personal, 
             pedido.estado, total_bs, pedido.observaciones)
        )
        id_pedido = await cur.fetchone()[0]
        
        # Insertar los detalles del pedido
        for detalle in detalles_con_precios:
            await cur.execute(
                '''INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario_bs, subtotal_bs, observaciones)
                   VALUES (%s, %s, %s, %s, %s, %s)''',
                (id_pedido, detalle['id_producto'], detalle['cantidad'], 
                 detalle['precio_unitario'], detalle['subtotal'], detalle['observaciones'])
            )
        
        return {
            'id_pedido': id_pedido,
            'total_bs': total_bs,
            'cantidad_productos': len(detalles_con_precios),
            'mensaje': 'Pedido creado exitosamente con sus detalles'
        }

@router.patch('/{id_pedido}/estado')
async def cambiar_estado_pedido(id_pedido: int, estado: str, conn = Depends(get_db)):
    """
    Cambiar el estado de un pedido.
    Estados válidos: pendiente, en_proceso, completado, entregado, cancelado
    """
    async with conn.cursor() as cur:
        await cur.execute(
            'UPDATE pedidos SET estado = %s WHERE id_pedido = %s RETURNING id_pedido, numero_pedido, estado',
            (estado, id_pedido)
        )
        resultado = await cur.fetchone()
        if resultado:
            return {
                'id_pedido': resultado[0],
                'numero_pedido': resultado[1],
                'nuevo_estado': resultado[2],
                'mensaje': f'Estado cambiado a: {estado}'
            }
        else:
            return {'error': 'Pedido no encontrado'}

@router.put('/{id}')
async def actualizar_pedido(id: int, pedido: Pedido, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute(
            '''UPDATE pedidos SET numero_pedido = %s, id_mesa = %s, id_personal = %s, 
               estado = %s, observaciones = %s WHERE id_pedido = %s''',
            (pedido.numero_pedido, pedido.id_mesa, pedido.id_personal, 
             pedido.estado, pedido.observaciones, id)
        )
        return {'mensaje': 'Pedido actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_pedido(id: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('UPDATE pedidos SET activo = FALSE WHERE id_pedido = %s', (id,))
        return {'mensaje': 'Pedido eliminado exitosamente'}
