from fastapi import APIRouter, Depends
from typing import Optional
from datetime import date
from config.conexionDB import get_db
from psycopg.rows import dict_row

router = APIRouter(prefix='/reportes', tags=['Reportes'])

@router.get('/general')
async def reporte_general(conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        # Calculamos el total sumando (cantidad * precio) de los detalles
        await cur.execute('''
            SELECT 
                COUNT(DISTINCT p.id_pedido) as total_pedidos,
                SUM(dp.cantidad * dp.precio_unitario_bs) as total_ventas_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.activo = TRUE AND p.estado != 'cancelado'
        ''')
        res_general = await cur.fetchone()

        await cur.execute('''
            SELECT 
                c.nombre as categoria,
                p.nombre as producto,
                SUM(dp.cantidad) as unidades,
                SUM(dp.cantidad * dp.precio_unitario_bs) as subtotal
            FROM detalle_pedidos dp
            JOIN productos p ON dp.id_producto = p.id_producto
            JOIN categorias c ON p.id_categoria = c.id_categoria
            JOIN pedidos ped ON dp.id_pedido = ped.id_pedido
            WHERE ped.activo = TRUE AND ped.estado != 'cancelado'
            GROUP BY c.nombre, p.nombre
            ORDER BY c.nombre, subtotal DESC
        ''')
        res_detallado = await cur.fetchall()

        return {
            'resumen_general': res_general,
            'ventas_detalladas': res_detallado
        }

@router.get('/diario')
async def reporte_diario(conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('''
            SELECT 
                COUNT(DISTINCT p.id_pedido) as total_pedidos,
                SUM(dp.cantidad * dp.precio_unitario_bs) as total_ventas_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.activo = TRUE AND p.estado != 'cancelado' 
            AND DATE(p.fecha_pedido) = CURRENT_DATE
        ''')
        res = await cur.fetchone()
        
        await cur.execute('''
            SELECT p.id_pedido, p.numero_pedido, m.numero as mesa, p.estado,
                   COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
            FROM pedidos p
            JOIN mesas m ON p.id_mesa = m.id_mesa
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.activo = TRUE AND DATE(p.fecha_pedido) = CURRENT_DATE
            GROUP BY p.id_pedido, m.numero
            ORDER BY p.fecha_pedido DESC
        ''')
        pedidos = await cur.fetchall()
        
        return {
            'resumen': res,
            'pedidos_hoy': pedidos
        }

@router.get('/individual/pedido/{id_pedido}')
async def reporte_pedido(id_pedido: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('''
            SELECT 
                p.id_pedido, p.numero_pedido, p.fecha_pedido as fecha, p.estado,
                m.numero as mesa,
                pers.nombre || ' ' || pers.apellido_paterno as mesero,
                COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
            FROM pedidos p
            JOIN mesas m ON p.id_mesa = m.id_mesa
            JOIN personal pers ON p.id_personal = pers.id_personal
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.id_pedido = %s AND p.activo = TRUE
            GROUP BY p.id_pedido, m.numero, pers.id_personal
        ''', (id_pedido,))
        pedido = await cur.fetchone()

        if not pedido:
            return {'error': 'Pedido no encontrado'}

        await cur.execute('''
            SELECT 
                dp.id_detalle, prod.nombre as producto,
                dp.cantidad, dp.precio_unitario_bs,
                (dp.cantidad * dp.precio_unitario_bs) as subtotal
            FROM detalle_pedidos dp
            JOIN productos prod ON dp.id_producto = prod.id_producto
            WHERE dp.id_pedido = %s
        ''', (id_pedido,))
        detalles = await cur.fetchall()

        return {
            'reporte_pedido': pedido,
            'detalles': detalles
        }

@router.get('/individual/personal/{id_personal}')
async def reporte_personal(id_personal: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('SELECT nombre, apellido_paterno FROM personal WHERE id_personal = %s', (id_personal,))
        personal = await cur.fetchone()
        
        if not personal:
            return {'error': 'Personal no encontrado'}

        await cur.execute('''
            SELECT 
                COUNT(DISTINCT p.id_pedido) as total_atendidos,
                SUM(dp.cantidad * dp.precio_unitario_bs) as total_generado_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.id_personal = %s AND p.activo = TRUE AND p.estado != 'cancelado'
        ''', (id_personal,))
        stats = await cur.fetchone()

        await cur.execute('''
            SELECT p.id_pedido, p.numero_pedido, p.fecha_pedido, p.estado,
                   COALESCE(SUM(dp.cantidad * dp.precio_unitario_bs), 0) as total_bs
            FROM pedidos p
            LEFT JOIN detalle_pedidos dp ON p.id_pedido = dp.id_pedido
            WHERE p.id_personal = %s AND p.activo = TRUE
            GROUP BY p.id_pedido
            ORDER BY p.fecha_pedido DESC
            LIMIT 10
        ''', (id_personal,))
        pedidos = await cur.fetchall()

        return {
            'empleado': personal,
            'estadisticas': stats,
            'ultimos_pedidos': pedidos
        }
