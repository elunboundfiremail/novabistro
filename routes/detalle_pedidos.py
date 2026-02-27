from fastapi import APIRouter, Depends
from config.conexionDB import get_db

router = APIRouter(prefix='/detalle_pedidos', tags=['Detalle Pedidos'])

@router.get('/')
async def listar_todos_los_detalles(conn = Depends(get_db)):
    """Ver TODOS los detalles de TODOS los pedidos con nombres legibles"""
    async with conn.cursor() as cur:
        await cur.execute(
            '''SELECT 
                dp.id_detalle,
                dp.id_pedido,
                p.numero_pedido,
                m.numero AS mesa,
                dp.id_producto,
                prod.nombre AS nombre_producto,
                dp.cantidad,
                dp.precio_unitario_bs,
                dp.subtotal_bs,
                dp.observaciones,
                ped.estado AS estado_pedido
               FROM detalle_pedidos dp
               JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
               JOIN productos prod ON dp.id_producto = prod.id_producto
               JOIN mesas m ON ped.id_mesa = m.id_mesa
               ORDER BY dp.id_pedido DESC, dp.id_detalle ASC'''
        )
        detalles = await cur.fetchall()
        
        return [
            {
                'id_detalle': d[0],
                'id_pedido': d[1],
                'numero_pedido': d[2],
                'mesa': d[3],
                'id_producto': d[4],
                'nombre_producto': d[5],
                'cantidad': d[6],
                'precio_unitario_bs': float(d[7]),
                'subtotal_bs': float(d[8]),
                'observaciones': d[9],
                'estado_pedido': d[10]
            }
            for d in detalles
        ]

@router.get('/pedido/{id_pedido}')
async def listar_detalles_por_pedido(id_pedido: int, conn = Depends(get_db)):
    """Ver los detalles de UN pedido específico"""
    async with conn.cursor() as cur:
        await cur.execute(
            '''SELECT 
                dp.id_detalle,
                dp.id_pedido,
                ped.numero_pedido,
                dp.id_producto,
                prod.nombre AS nombre_producto,
                dp.cantidad,
                dp.precio_unitario_bs,
                dp.subtotal_bs,
                dp.observaciones
               FROM detalle_pedidos dp
               JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
               JOIN productos prod ON dp.id_producto = prod.id_producto
               WHERE dp.id_pedido = %s
               ORDER BY dp.id_detalle ASC''',
            (id_pedido,)
        )
        detalles = await cur.fetchall()
        
        return [
            {
                'id_detalle': d[0],
                'id_pedido': d[1],
                'numero_pedido': d[2],
                'id_producto': d[3],
                'nombre_producto': d[4],
                'cantidad': d[5],
                'precio_unitario_bs': float(d[6]),
                'subtotal_bs': float(d[7]),
                'observaciones': d[8]
            }
            for d in detalles
        ]
