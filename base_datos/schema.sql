-- Base de datos: novabistro
-- Script de Estructura y Datos Base

DROP TABLE IF EXISTS detalle_pedidos CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS mesas CASCADE;
DROP TABLE IF EXISTS personal CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- ESTRUCTURA
CREATE TABLE roles (
    id_rol INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE personal (
    id_personal INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ci BIGINT UNIQUE NOT NULL,
    password VARCHAR(100) DEFAULT '$2b$12$clZ.Y.REPyvSRNQ8.YmUp.vXm2G6.YmUp.vXm2G6.YmUp.vXm2G6', -- pass: 123456
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccion TEXT,
    id_rol INTEGER REFERENCES roles(id_rol),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE mesas (
    id_mesa INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    numero INTEGER UNIQUE NOT NULL,
    capacidad INTEGER NOT NULL,
    ubicacion VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'disponible',
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_bs DECIMAL(10, 2) NOT NULL,
    id_categoria INTEGER REFERENCES categorias(id_categoria),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    numero_pedido VARCHAR(20) UNIQUE,
    id_mesa INTEGER REFERENCES mesas(id_mesa),
    id_personal INTEGER REFERENCES personal(id_personal),
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente',
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE detalle_pedidos (
    id_detalle INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_pedido INTEGER REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario_bs DECIMAL(10, 2) NOT NULL,
    observaciones TEXT
);

-- DATOS INICIALES (SOLO CATÁLOGOS Y PERSONAL)

INSERT INTO roles (nombre, descripcion) VALUES 
('Administrador', 'Acceso total'),
('Mesero', 'Atencion salón'),
('Cocinero', 'Produccion platos'),
('Cajero', 'Cobros y facturacion');

INSERT INTO personal (ci, nombre, apellido_paterno, id_rol) VALUES 
(123, 'Admin', 'Sistema', 1),
(456, 'Juan', 'Perez', 2),
(789, 'Maria', 'Gomez', 3);

INSERT INTO categorias (nombre) VALUES 
('Entradas'), ('Platos Fuertes'), ('Bebidas'), ('Postres'), ('Sopas');

INSERT INTO productos (nombre, precio_bs, id_categoria) VALUES 
('Nachos con Queso', 25.00, 1),
('Alitas BBQ', 35.00, 1),
('Pique Macho', 65.00, 2),
('Silpancho', 45.00, 2),
('Limonada', 15.00, 3),
('Cerveza Paceña', 20.00, 3),
('Helado de Vainilla', 18.00, 4),
('Sopa de Mani', 22.00, 5);

INSERT INTO mesas (numero, capacidad, ubicacion) VALUES 
(1, 4, 'Salon'), (2, 4, 'Salon'), (3, 2, 'Salon'), (4, 2, 'Ventana'), (5, 6, 'Terraza'),
(6, 4, 'Terraza'), (7, 4, 'Salon'), (8, 4, 'Salon'), (9, 2, 'Bar'), (10, 2, 'Bar'),
(11, 4, 'Salon'), (12, 4, 'Salon'), (13, 6, 'VIP'), (14, 4, 'VIP'), (15, 2, 'Salon'),
(16, 4, 'Salon'), (17, 4, 'Salon'), (18, 4, 'Salon'), (19, 4, 'Salon'), (20, 8, 'VIP');
