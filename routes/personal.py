from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import date
from config.conexionDB import get_db
from psycopg.rows import dict_row
import bcrypt

router = APIRouter(prefix='/personal', tags=['Personal'])

class Personal(BaseModel):
    ci: int
    password: Optional[str] = '123456'
    nombre: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    id_rol: int

class Login(BaseModel):
    ci: int
    password: str

@router.post('/login')
async def login(datos: Login, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            'SELECT id_personal, ci, nombre, id_rol, password FROM personal WHERE ci = %s AND activo = TRUE',
            (datos.ci,)
        )
        user = await cur.fetchone()
        
        if user:
            password_db = user['password'].encode('utf-8')
            password_ingresada = datos.password.encode('utf-8')
            
            if bcrypt.checkpw(password_ingresada, password_db):
                return {
                    'id_personal': user['id_personal'],
                    'ci': user['ci'],
                    'nombre': user['nombre'],
                    'id_rol': user['id_rol'],
                    'mensaje': 'Acceso concedido'
                }
        
        raise HTTPException(status_code=401, detail='Credenciales invalidas')

@router.get('/')
async def listar_personal(conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('SELECT id_personal, ci, nombre, apellido_paterno, apellido_materno, telefono, email, direccion, id_rol FROM personal WHERE activo = TRUE')
        personal = await cur.fetchall()
        return personal

@router.post('/')
async def crear_personal(persona: Personal, conn = Depends(get_db)):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(persona.password.encode('utf-8'), salt).decode('utf-8')
    
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            '''INSERT INTO personal (ci, password, nombre, apellido_paterno, apellido_materno, 
               fecha_nacimiento, direccion, telefono, email, id_rol) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_personal''',
            (persona.ci, hash_password, persona.nombre, persona.apellido_paterno, persona.apellido_materno,
             persona.fecha_nacimiento, persona.direccion, persona.telefono, persona.email, persona.id_rol)
        )
        id_personal = await cur.fetchone()
        return {'id_personal': id_personal['id_personal'], 'mensaje': 'Personal creado exitosamente'}

@router.put('/{id}')
async def actualizar_personal(id: int, persona: Personal, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute(
            '''UPDATE personal SET ci = %s, nombre = %s, apellido_paterno = %s, 
               apellido_materno = %s, fecha_nacimiento = %s, direccion = %s, 
               telefono = %s, email = %s, id_rol = %s WHERE id_personal = %s''',
            (persona.ci, persona.nombre, persona.apellido_paterno, persona.apellido_materno,
             persona.fecha_nacimiento, persona.direccion, persona.telefono, persona.email, 
             persona.id_rol, id)
        )
        return {'mensaje': 'Personal actualizado exitosamente'}

@router.delete('/{id}')
async def eliminar_personal(id: int, conn = Depends(get_db)):
    async with conn.cursor(row_factory=dict_row) as cur:
        await cur.execute('UPDATE personal SET activo = FALSE WHERE id_personal = %s', (id,))
        return {'mensaje': 'Personal eliminado exitosamente'}
