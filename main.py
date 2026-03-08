from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.conexionDB import lifespan
from routes import roles, personal, mesas, categorias, productos, pedidos, reportes

app = FastAPI(
    title='NovaBistro API',
    description='Sistema de gestion para restaurante',
    version='1.0.0',
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(roles.router)
app.include_router(personal.router)
app.include_router(mesas.router)
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(pedidos.router)
app.include_router(reportes.router)

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
            '/reportes'
        ]
    }
