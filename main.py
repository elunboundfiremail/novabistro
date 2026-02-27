from fastapi import FastAPI
from config.conexionDB import lifespan
from routes import roles, personal, mesas, categorias, productos, pedidos, detalle_pedidos

app = FastAPI(
    title='NovaBistro API',
    description='Sistema de gestion para restaurante',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(roles.router)
app.include_router(personal.router)
app.include_router(mesas.router)
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(pedidos.router)
app.include_router(detalle_pedidos.router)

@app.get('/')
async def root():
    return {
        'mensaje': 'Bienvenido a NovaBistro API',
        'version': '1.0.0',
        'endpoints': [
            '/roles',
            '/personal',
            '/mesas',
            '/categorias',
            '/productos',
            '/pedidos',
            '/detalle_pedidos'
        ]
    }
