import bcrypt
import asyncio
import selectors
import psycopg

async def reparar():
    # El hash correcto para '123456'
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw("123456".encode('utf-8'), salt).decode('utf-8')
    
    conn_info = 'postgresql://postgres:12345678@localhost:5432/novabistro'
    
    try:
        # Conexión directa sin pool para evitar errores de bucle
        conn = await psycopg.AsyncConnection.connect(conn_info)
        async with conn.cursor() as cur:
            # Actualizar a todos los empleados
            await cur.execute("UPDATE personal SET password = %s, activo = TRUE", (hash_password,))
            print(f"ÉXITO: Todos los empleados ahora tienen la clave: 123456")
            print(f"Hash generado: {hash_password}")
            await conn.commit()
        await conn.close()
    except Exception as e:
        print(f"Error al conectar: {e}")

if __name__ == "__main__":
    # Forzar el SelectorEventLoop para compatibilidad en Windows
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(reparar())
    finally:
        loop.close()
