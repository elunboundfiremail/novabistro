from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool

pool = None

@asynccontextmanager
async def lifespan(app):
    global pool
    pool = AsyncConnectionPool(
        conninfo='postgresql://postgres:12345678@localhost:5432/novabistro',
        min_size=1,
        max_size=10,
        open=True
    )
    yield
    await pool.close()

async def get_db():
    async with pool.connection() as conn:
        yield conn
