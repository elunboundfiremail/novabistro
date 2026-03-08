from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from config.conexionDB import get_db
from psycopg.rows import dict_row

router = APIRouter(prefix='/pedidos', tags=['Pedidos'])

class DetallePedido(BaseModel):
    id_producto: int
    cantidad: int
    observaciones: Optional[str] = None

class Pedido(BaseModel):
    numero_pedido: Optional[str] = None
    id_mesa: int
    id_personal: int
    estado: Optional[str] = 'pendiente'
    observaciones: Optional[str] = None
    detalles: List[DetallePedido] = []

@router.get('/')
async def listar_pedidos(conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('''
            SELECT p.*, COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.activo = TRUE 
            GROUP BY p.id_pedido
            ORDER BY p.fecha_pedido DESC
        ''')
        pedidos = await cur.fetchall()
        return pedidos

@router.get('/estado/{estado}')
async def listar_pedidos_por_estado(estado: str, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('''
            SELECT p.*, COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.estado = %s AND p.activo = TRUE
            GROUP BY p.id_pedido
        ''', (estado,))
        pedidos = await cur.fetchall()
        return pedidos

@router.get('/detalle/{id_pedido}')
async def obtener_pedido_con_detalles(id_pedido: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            '''SELECT p.id_pedido, p.numero_pedido, p.id_mesa, p.id_personal, 
                      p.fecha_pedido, p.estado, p.observaciones,
                      COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
               FROM pedidos p 
               LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
               WHERE p.id_pedido = %s AND p.activo = TRUE
               GROUP BY p.id_pedido''',
            (id_pedido,)
        )
        pedido = await cur.fetchone()
        
        if not pedido:
            return {'error': 'Pedido no encontrado'}
        
        await cur.execute(
            '''SELECT dp.id_detalle, dp.id_producto, pr.nombre AS producto,
                      dp.cantidad, dp.precio_unitario_bs, 
                      (dp.cantidad * dp.precio_unitario_bs) as subtotal_bs, dp.observaciones
               FROM detalle_pedidos dp
               JOIN productos pr ON dp.id_producto = pr.id_producto
               WHERE dp.id_pedido = %s''',
            (id_pedido,)
        )
        detalles = await cur.fetchall()
        
        return {
            'pedido': pedido,
            'detalles': detalles
        }

@router.post('/')
async def crear_pedido(pedido: Pedido, conn = Depends(get_db)):
    try:
        async with conn.cursor(row_factory=dict_row) as cur:
            detalles_con_precios = []
            
            for detalle in pedido.detalles:
                await cur.execute(
                    'SELECT precio_bs FROM productos WHERE id_producto = %s AND activo = TRUE',
                    (detalle.id_producto,)
                )
                resultado = await cur.fetchone()
                if resultado:
                    precio_unitario = float(resultado['precio_bs'])
                    detalles_con_precios.append({
                        'id_producto': detalle.id_producto,
                        'cantidad': detalle.cantidad,
                        'precio_unitario': precio_unitario,
                        'observaciones': detalle.observaciones
                    })
                else:
                    return {'error': f'Producto con ID {detalle.id_producto} no encontrado'}
            
            await cur.execute(
                '''INSERT INTO pedidos (id_mesa, id_personal, estado, observaciones) 
                   VALUES (%s, %s, %s, %s) RETURNING id_pedido''',
                (pedido.id_mesa, pedido.id_personal, 
                 pedido.estado, pedido.observaciones)
            )
            id_pedido_row = await cur.fetchone()
            id_pedido = id_pedido_row['id_pedido']
            
            fecha_str = datetime.now().strftime('%Y%m%d')
            nuevo_codigo = f'PED-{fecha_str}-{id_pedido}'
            
            await cur.execute(
                'UPDATE pedidos SET numero_pedido = %s WHERE id_pedido = %s',
                (nuevo_codigo, id_pedido)
            )
            
            for detalle in detalles_con_precios:
                await cur.execute(
                    '''INSERT INTO detalle_pedidos (id_pedido, id_producto, cantidad, precio_unitario_bs, observaciones)
                       VALUES (%s, %s, %s, %s, %s)''',
                    (id_pedido, detalle['id_producto'], detalle['cantidad'], 
                     detalle['precio_unitario'], detalle['observaciones'])
                )
            
            return {
                'id_pedido': id_pedido,
                'numero_pedido': nuevo_codigo,
                'mensaje': 'Pedido creado exitosamente'
            }
    except Exception as e:
        return {'error': str(e)}

@router.put('/{id_pedido}/estado')
async def cambiar_estado_pedido(id_pedido: int, estado: str, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            'UPDATE pedidos SET estado = %s WHERE id_pedido = %s RETURNING id_pedido, numero_pedido, estado',
            (estado, id_pedido)
        )
        resultado = await cur.fetchone()
        if resultado:
            return resultado
        else:
            return {'error': 'Pedido no encontrado'}

@router.put('/{id}')
async def actualizar_pedido(id: int, pedido: Pedido, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            '''UPDATE pedidos SET numero_pedido = %s, id_mesa = %s, id_personal = %s, 
               estado = %s, observaciones = %s WHERE id_pedido = %s''',
            (pedido.numero_pedido, pedido.id_mesa, pedido.id_personal, 
             pedido.estado, pedido.observaciones, id)
        )
        return {'mensaje': 'Pedido actualizado exitosamente'}

@router.get('/mesa/{id_mesa}/activo')
async def obtener_pedido_activo_mesa(id_mesa: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            '''SELECT id_pedido, numero_pedido, observaciones 
               FROM pedidos WHERE id_mesa = %s AND estado IN ('pendiente', 'en_proceso', 'completado') 
               AND activo = TRUE ORDER BY fecha_pedido DESC LIMIT 1''',
            (id_mesa,)
        )
        pedido = await cur.fetchone()
        if not pedido:
            return None
        
        await cur.execute(
            '''SELECT dp.id_detalle, pr.nombre AS producto, dp.cantidad, 
                      (dp.cantidad * dp.precio_unitario_bs) as subtotal_bs, dp.observaciones 
               FROM detalle_pedidos dp
               JOIN productos pr ON dp.id_producto = pr.id_producto
               WHERE dp.id_pedido = %s''',
            (pedido['id_pedido'],)
        )
        detalles = await cur.fetchall()
        
        total_bs = sum(float(d['subtotal_bs']) for d in detalles)
        pedido['total_bs'] = total_bs
        
        return {'pedido': pedido, 'detalles': detalles}

@router.delete('/{id}')
async def eliminar_pedido(id: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('UPDATE pedidos SET activo = FALSE WHERE id_pedido = %s', (id,))
        return {'mensaje': 'Pedido eliminado exitosamente'}
