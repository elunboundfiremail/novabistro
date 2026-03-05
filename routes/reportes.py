from fastapi import APIRouter, Depends
from typing import Optional
from datetime import date
from config.conexionDB import get_db

router = APIRouter(prefix='/reportes', tags=['Reportes'])

@router.get('/general')
async def reporte_general(conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('''
            SELECT 
                COUNT(*) as total_pedidos,
                SUM(total_bs) as total_ventas_bs,
                AVG(total_bs) as promedio_por_pedido
            FROM pedidos 
            WHERE activo = TRUE AND estado != 'cancelado'
        ''')
        res_general = await cur.fetchone()
        
        await cur.execute('''
            SELECT 
                c.nombre as categoria,
                COUNT(dp.id_detalle) as cantidad_vendida,
                SUM(dp.subtotal_bs) as total_bs
            FROM detalle_pedidos dp
            JOIN productos p ON dp.id_producto = p.id_producto
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
            WHERE ped.activo = TRUE AND ped.estado != 'cancelado'
            GROUP BY c.nombre
            ORDER BY total_bs DESC
        ''')
        res_categorias = await cur.fetchall()
        
        await cur.execute('''
            SELECT 
                p.nombre as producto,
                SUM(dp.cantidad) as cantidad_total,
                SUM(dp.subtotal_bs) as total_generado_bs
            FROM detalle_pedidos dp
            JOIN productos p ON dp.id_producto = p.id_producto
            JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
            WHERE ped.activo = TRUE AND ped.estado != 'cancelado'
            GROUP BY p.nombre
            ORDER BY cantidad_total DESC
            LIMIT 5
        ''')
        res_productos = await cur.fetchall()

        return {
            'resumen_general': {
                'total_pedidos': res_general[0] or 0,
                'total_ventas_bs': float(res_general[1] or 0),
                'promedio_pedido_bs': float(res_general[2] or 0)
            },
            'ventas_por_categoria': [
                {'categoria': r[0], 'cantidad': r[1], 'total_bs': float(r[2])}
                for r in res_categorias
            ],
            'top_productos': [
                {'producto': r[0], 'cantidad': r[1], 'total_bs': float(r[2])}
                for r in res_productos
            ]
        }

@router.get('/individual/pedido/{id_pedido}')
async def reporte_individual_pedido(id_pedido: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('''
            SELECT 
                p.numero_pedido, 
                p.fecha_pedido, 
                p.estado, 
                p.total_bs, 
                p.observaciones,
                m.numero as numero_mesa,
                per.nombre || ' ' || per.apellido_paterno as mesero
            FROM pedidos p
            JOIN mesas m ON p.id_mesa = m.id_mesa
            JOIN personal per ON p.id_personal = per.id_personal
            WHERE p.id_pedido = %s AND p.activo = TRUE
        ''', (id_pedido,))
        pedido = await cur.fetchone()
        
        if not pedido:
            return {'error': 'Pedido no encontrado'}
            
        await cur.execute('''
            SELECT 
                prod.nombre, 
                dp.cantidad, 
                dp.precio_unitario_bs, 
                dp.subtotal_bs,
                dp.observaciones
            FROM detalle_pedidos dp
            JOIN productos prod ON dp.id_producto = prod.id_producto
            WHERE dp.id_pedido = %s
        ''', (id_pedido,))
        detalles = await cur.fetchall()
        
        return {
            'reporte_pedido': {
                'numero_pedido': pedido[0],
                'fecha': str(pedido[1]),
                'estado': pedido[2],
                'total_bs': float(pedido[3]),
                'observaciones': pedido[4],
                'mesa': pedido[5],
                'mesero': pedido[6]
            },
            'detalles': [
                {
                    'producto': d[0],
                    'cantidad': d[1],
                    'precio_unitario': float(d[2]),
                    'subtotal': float(d[3]),
                    'nota': d[4]
                }
                for d in detalles
            ]
        }

@router.get('/individual/personal/{id_personal}')
async def reporte_ventas_personal(id_personal: int, conn = Depends(get_db)):
    async with conn.cursor() as cur:
        await cur.execute('SELECT nombre, apellido_paterno FROM personal WHERE id_personal = %s', (id_personal,))
        pers = await cur.fetchone()
        if not pers:
            return {'error': 'Personal no encontrado'}
            
        await cur.execute('''
            SELECT 
                COUNT(*) as total_pedidos,
                SUM(total_bs) as total_ventas_bs
            FROM pedidos 
            WHERE id_personal = %s AND activo = TRUE AND estado != 'cancelado'
        ''', (id_personal,))
        stats = await cur.fetchone()
        
        await cur.execute('''
            SELECT numero_pedido, fecha_pedido, total_bs, estado
            FROM pedidos 
            WHERE id_personal = %s AND activo = TRUE
            ORDER BY fecha_pedido DESC
            LIMIT 10
        ''', (id_personal,))
        pedidos = await cur.fetchall()
        
        return {
            'personal': f'{pers[0]} {pers[1]}',
            'resumen': {
                'total_pedidos': stats[0] or 0,
                'total_generado_bs': float(stats[1] or 0)
            },
            'ultimos_pedidos': [
                {'numero': p[0], 'fecha': str(p[1]), 'total': float(p[2]), 'estado': p[3]}
                for p in pedidos
            ]
        }
