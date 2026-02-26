-- Base de datos: novabistro
-- Sistema de gestion para restaurante

-- Eliminar tablas si existen (en orden inverso por dependencias)
DROP TABLE IF EXISTS detalle_pedidos CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;
DROP TABLE IF EXISTS mesas CASCADE;
DROP TABLE IF EXISTS personal CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- Tabla de roles
CREATE TABLE roles (
    id_rol INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de personal
CREATE TABLE personal (
    id_personal INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ci VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    fecha_nacimiento DATE,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    id_rol INTEGER REFERENCES roles(id_rol),
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de mesas
CREATE TABLE mesas (
    id_mesa INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    numero INTEGER UNIQUE NOT NULL,
    capacidad INTEGER NOT NULL,
    ubicacion VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'disponible',
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de categorias
CREATE TABLE categorias (
    id_categoria INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de productos
CREATE TABLE productos (
    id_producto INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio_bs DECIMAL(10, 2) NOT NULL,
    id_categoria INTEGER REFERENCES categorias(id_categoria),
    disponible BOOLEAN DEFAULT TRUE,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de pedidos
CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    numero_pedido VARCHAR(20) UNIQUE NOT NULL,
    id_mesa INTEGER REFERENCES mesas(id_mesa),
    id_personal INTEGER REFERENCES personal(id_personal),
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente',
    total_bs DECIMAL(10, 2) DEFAULT 0.00,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de detalle de pedidos
CREATE TABLE detalle_pedidos (
    id_detalle INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    id_pedido INTEGER REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    id_producto INTEGER REFERENCES productos(id_producto),
    cantidad INTEGER NOT NULL,
    precio_unitario_bs DECIMAL(10, 2) NOT NULL,
    subtotal_bs DECIMAL(10, 2) NOT NULL,
    observaciones TEXT
);

-- Indices para mejorar rendimiento
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
CREATE INDEX idx_pedidos_mesa ON pedidos(id_mesa);
CREATE INDEX idx_productos_categoria ON productos(id_categoria);
CREATE INDEX idx_detalle_pedido ON detalle_pedidos(id_pedido);
CREATE INDEX idx_personal_rol ON personal(id_rol);

-- Insertar datos de ejemplo
INSERT INTO roles (nombre, descripcion) VALUES 
('Administrador', 'Acceso total al sistema'),
('Mesero', 'Personal de atencion al cliente'),
('Cocinero', 'Personal de cocina'),
('Cajero', 'Personal de caja');

INSERT INTO categorias (nombre, descripcion) VALUES 
('Entradas', 'Platos de entrada'),
('Platos principales', 'Platos fuertes del menu'),
('Bebidas', 'Bebidas frias y calientes'),
('Postres', 'Postres y dulces'),
('Sopas', 'Sopas tradicionales');

INSERT INTO mesas (numero, capacidad, ubicacion) VALUES 
(1, 4, 'Salon principal'),
(2, 4, 'Salon principal'),
(3, 2, 'Salon principal'),
(4, 6, 'Terraza'),
(5, 4, 'Terraza'),
(6, 8, 'Salon VIP');

-- Mensaje de confirmacion
DO $$
BEGIN
    RAISE NOTICE 'Base de datos novabistro creada exitosamente';
    RAISE NOTICE 'Tablas creadas: roles, personal, mesas, categorias, productos, pedidos, detalle_pedidos';
    RAISE NOTICE 'Datos de ejemplo insertados';
END $$;
