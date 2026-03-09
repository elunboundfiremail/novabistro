--
-- PostgreSQL database dump
--

\restrict WQ2EI8msZcp4AtzeF67wkitquoBwM5lJEwnQ6vsf80HOobJUmPaeFJnaffJbECs

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.productos DROP CONSTRAINT IF EXISTS productos_id_categoria_fkey;
ALTER TABLE IF EXISTS ONLY public.personal DROP CONSTRAINT IF EXISTS personal_id_rol_fkey;
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS pedidos_id_personal_fkey;
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS pedidos_id_mesa_fkey;
ALTER TABLE IF EXISTS ONLY public.detalle_pedidos DROP CONSTRAINT IF EXISTS detalle_pedidos_id_producto_fkey;
ALTER TABLE IF EXISTS ONLY public.detalle_pedidos DROP CONSTRAINT IF EXISTS detalle_pedidos_id_pedido_fkey;
DROP INDEX IF EXISTS public.idx_productos_categoria;
DROP INDEX IF EXISTS public.idx_personal_rol;
DROP INDEX IF EXISTS public.idx_pedidos_mesa;
DROP INDEX IF EXISTS public.idx_pedidos_estado;
DROP INDEX IF EXISTS public.idx_detalle_pedido;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_pkey;
ALTER TABLE IF EXISTS ONLY public.roles DROP CONSTRAINT IF EXISTS roles_nombre_key;
ALTER TABLE IF EXISTS ONLY public.productos DROP CONSTRAINT IF EXISTS productos_pkey;
ALTER TABLE IF EXISTS ONLY public.personal DROP CONSTRAINT IF EXISTS personal_pkey;
ALTER TABLE IF EXISTS ONLY public.personal DROP CONSTRAINT IF EXISTS personal_email_key;
ALTER TABLE IF EXISTS ONLY public.personal DROP CONSTRAINT IF EXISTS personal_ci_key;
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS pedidos_pkey;
ALTER TABLE IF EXISTS ONLY public.pedidos DROP CONSTRAINT IF EXISTS pedidos_numero_pedido_key;
ALTER TABLE IF EXISTS ONLY public.mesas DROP CONSTRAINT IF EXISTS mesas_pkey;
ALTER TABLE IF EXISTS ONLY public.mesas DROP CONSTRAINT IF EXISTS mesas_numero_key;
ALTER TABLE IF EXISTS ONLY public.detalle_pedidos DROP CONSTRAINT IF EXISTS detalle_pedidos_pkey;
ALTER TABLE IF EXISTS ONLY public.categorias DROP CONSTRAINT IF EXISTS categorias_pkey;
ALTER TABLE IF EXISTS ONLY public.categorias DROP CONSTRAINT IF EXISTS categorias_nombre_key;
DROP TABLE IF EXISTS public.roles;
DROP TABLE IF EXISTS public.productos;
DROP TABLE IF EXISTS public.personal;
DROP TABLE IF EXISTS public.pedidos;
DROP TABLE IF EXISTS public.mesas;
DROP TABLE IF EXISTS public.detalle_pedidos;
DROP TABLE IF EXISTS public.categorias;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categorias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categorias (
    id_categoria integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    activo boolean DEFAULT true
);


ALTER TABLE public.categorias OWNER TO postgres;

--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.categorias ALTER COLUMN id_categoria ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.categorias_id_categoria_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: detalle_pedidos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalle_pedidos (
    id_detalle integer NOT NULL,
    id_pedido integer,
    id_producto integer,
    cantidad integer NOT NULL,
    precio_unitario_bs numeric(10,2) NOT NULL,
    observaciones text
);


ALTER TABLE public.detalle_pedidos OWNER TO postgres;

--
-- Name: detalle_pedidos_id_detalle_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.detalle_pedidos ALTER COLUMN id_detalle ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.detalle_pedidos_id_detalle_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: mesas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mesas (
    id_mesa integer NOT NULL,
    numero integer NOT NULL,
    capacidad integer NOT NULL,
    ubicacion character varying(50),
    estado character varying(20) DEFAULT 'disponible'::character varying,
    activo boolean DEFAULT true
);


ALTER TABLE public.mesas OWNER TO postgres;

--
-- Name: mesas_id_mesa_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.mesas ALTER COLUMN id_mesa ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.mesas_id_mesa_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: pedidos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedidos (
    id_pedido integer NOT NULL,
    numero_pedido character varying(20),
    id_mesa integer,
    id_personal integer,
    fecha_pedido timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado character varying(20) DEFAULT 'pendiente'::character varying,
    observaciones text,
    activo boolean DEFAULT true
);


ALTER TABLE public.pedidos OWNER TO postgres;

--
-- Name: pedidos_id_pedido_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.pedidos ALTER COLUMN id_pedido ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.pedidos_id_pedido_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: personal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.personal (
    id_personal integer NOT NULL,
    ci bigint NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido_paterno character varying(100) NOT NULL,
    apellido_materno character varying(100),
    fecha_nacimiento date,
    direccion text,
    telefono character varying(20),
    email character varying(100),
    id_rol integer,
    activo boolean DEFAULT true,
    password character varying(100) DEFAULT '123456'::character varying
);


ALTER TABLE public.personal OWNER TO postgres;

--
-- Name: personal_id_personal_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.personal ALTER COLUMN id_personal ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.personal_id_personal_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: productos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.productos (
    id_producto integer NOT NULL,
    nombre character varying(150) NOT NULL,
    descripcion text,
    precio_bs numeric(10,2) NOT NULL,
    id_categoria integer,
    disponible boolean DEFAULT true,
    activo boolean DEFAULT true
);


ALTER TABLE public.productos OWNER TO postgres;

--
-- Name: productos_id_producto_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.productos ALTER COLUMN id_producto ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.productos_id_producto_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    id_rol integer NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion text,
    activo boolean DEFAULT true
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: roles_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.roles ALTER COLUMN id_rol ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.roles_id_rol_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: categorias; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categorias (id_categoria, nombre, descripcion, activo) FROM stdin;
1	Entradas	Aperitivos y entradas para comenzar la comida	t
2	Sopas	Sopas tradicionales bolivianas y cremas	t
3	Platos Principales	Platos fuertes del menú, especialidades de la casa	t
4	Parrilladas	Carnes a la parrilla y especialidades	t
5	Platos Vegetarianos	Opciones sin carne para vegetarianos	t
6	Postres	Postres tradicionales y dulces	t
7	Bebidas Calientes	Café, té y bebidas calientes	t
8	Bebidas Frías	Jugos naturales, refrescos y bebidas frías	t
9	Cócteles Sin Alcohol	Bebidas especiales sin alcohol	t
\.


--
-- Data for Name: detalle_pedidos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalle_pedidos (id_detalle, id_pedido, id_producto, cantidad, precio_unitario_bs, observaciones) FROM stdin;
1	1	6	2	25.00	Sin picante
2	1	11	1	45.00	\N
3	1	12	1	38.00	\N
4	1	35	2	15.00	\N
5	1	26	2	15.00	\N
6	2	1	4	35.00	\N
7	2	19	1	220.00	\N
8	2	15	2	48.00	\N
9	2	28	2	22.00	\N
10	2	42	4	26.00	\N
11	3	3	4	16.00	2 de carne, 2 de pollo
12	3	31	2	13.00	\N
13	4	7	3	30.00	\N
14	4	13	2	35.00	\N
15	4	37	3	8.00	\N
16	4	26	2	15.00	\N
17	5	2	3	18.00	\N
18	5	18	3	65.00	\N
19	5	36	3	16.00	\N
20	6	10	2	22.00	\N
21	6	22	2	32.00	\N
22	6	24	1	38.00	\N
23	6	35	2	15.00	\N
24	6	27	2	18.00	\N
25	7	1	5	35.00	\N
26	7	19	1	220.00	\N
27	7	16	2	55.00	\N
28	7	28	5	22.00	\N
29	7	40	5	25.00	\N
30	13	1	2	35.00	Bien cocido
31	13	3	1	16.00	Fria
32	14	1	2	35.00	Sin cebolla
33	14	3	1	16.00	Bien helada
34	15	1	2	35.00	Sin cebolla
35	15	3	1	16.00	Bien helada
36	16	6	2	25.00	
37	16	17	2	65.00	
38	16	36	1	16.00	Bien helada
39	19	3	1	16.00	\N
40	19	3	1	16.00	\N
41	19	3	1	16.00	\N
42	19	5	1	14.00	\N
43	19	5	1	14.00	\N
44	19	5	1	14.00	\N
45	19	6	1	25.00	\N
46	20	3	7	16.00	
47	20	2	4	18.00	
48	21	41	1	25.00	
49	21	23	1	38.00	
50	21	33	1	10.00	
51	22	7	1	30.00	
52	22	17	1	65.00	
53	22	19	1	58.00	
54	23	7	1	30.00	
55	23	10	1	22.00	
56	23	2	1	18.00	
57	24	11	2	45.00	
58	24	2	1	18.00	
59	24	9	3	26.00	
60	24	8	1	28.00	
\.


--
-- Data for Name: mesas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mesas (id_mesa, numero, capacidad, ubicacion, estado, activo) FROM stdin;
2	2	2	Salón Principal	disponible	t
4	4	4	Salón Principal	disponible	t
5	5	4	Salón Principal	disponible	t
8	8	6	Salón Principal	disponible	t
9	9	8	Salón Principal	disponible	t
12	12	2	Terraza	disponible	t
16	16	6	Terraza	disponible	t
17	17	4	Salón VIP	disponible	t
18	18	4	Salón VIP	disponible	t
3	3	4	Salón Principal	disponible	t
11	11	2	Terraza	disponible	t
19	19	8	Salón VIP	disponible	t
13	13	4	Terraza	disponible	t
7	7	6	Salón Principal	disponible	t
15	15	6	Terraza	disponible	t
20	20	10	Salón VIP	disponible	t
1	1	2	Salón Principal	ocupada	t
10	10	8	Salón Principal	ocupada	t
14	14	4	Terraza	ocupada	t
6	6	4	Salón Principal	disponible	t
\.


--
-- Data for Name: pedidos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedidos (id_pedido, numero_pedido, id_mesa, id_personal, fecha_pedido, estado, observaciones, activo) FROM stdin;
4	PED-2026-004	7	3	2026-02-27 13:15:00	en_preparacion	Cliente tiene prisa	t
5	PED-2026-005	15	4	2026-02-27 14:30:00	servido	\N	t
7	PED-2026-007	20	4	2026-02-27 20:00:00	en_preparacion	Evento corporativo - 10 personas	t
1	PED-2026-001	3	3	2026-02-27 12:30:00	entregado	Cliente solicitó sin picante	t
8	PED-DESAYUNO-LIGERO	3	3	2026-02-27 11:10:53.827876	entregado	Cliente a dieta - porciones normales	t
3	PED-2026-003	11	5	2026-02-27 08:15:00	entregado	\N	t
2	PED-2026-002	19	4	2026-02-27 19:45:00	entregado	Mesa VIP - Servicio especial	t
14	PED-2026-1005	1	1	2026-03-05 09:08:01.48052	entregado	Cliente pide factura	t
15	PED-2026-2005	1	1	2026-03-05 09:32:19.669307	entregado	Cliente pide factura	t
16	PED-2026-6005	1	1	2026-03-05 10:58:57.221522	entregado	Cliente pide sin factura	t
13	PED-2026-1001	1	1	2026-03-05 08:49:04.990577	entregado	Cliente en mesa principal	t
20	PED-20260307-20	13	2	2026-03-07 23:39:32.090543	entregado	\N	t
6	PED-2026-006	1	5	2026-02-27 12:00:00	entregado	Cliente vegetariano estricto	t
19	PED-20260307-19	13	2	2026-03-07 23:23:29.246335	entregado	\N	t
21	PED-20260308-21	1	1	2026-03-08 04:34:32.330267	pendiente	\N	t
23	PED-20260308-23	14	1	2026-03-08 04:34:54.555674	pendiente	\N	t
22	PED-20260308-22	10	1	2026-03-08 04:34:46.127268	completado	\N	t
24	PED-20260308-24	6	2	2026-03-08 04:53:17.471991	entregado	\N	t
\.


--
-- Data for Name: personal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personal (id_personal, ci, nombre, apellido_paterno, apellido_materno, fecha_nacimiento, direccion, telefono, email, id_rol, activo, password) FROM stdin;
4	4567890	Ana	Ramírez	Condori	1997-02-28	Sopocachi, Av. 20 de Octubre #234	73456789	ana.ramirez@novabistro.com	2	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
5	5678901	Luis	Vargas	Mamani	1996-09-05	Miraflores, Calle Montevideo #567	74567890	luis.vargas@novabistro.com	2	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
6	6789012	Pedro	Sánchez	Quispe	1990-04-18	El Alto, Ciudad Satélite #890	75678901	pedro.sanchez@novabistro.com	3	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
7	7890123	Rosa	Flores	Choque	1992-12-30	Villa Fátima, Calle 3 #123	76789012	rosa.flores@novabistro.com	3	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
8	8901234	Miguel	Castro	Apaza	1994-06-14	Obrajes, Av. Costanera #345	77890123	miguel.castro@novabistro.com	4	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
9	9012345	Laura	Morales	Huanca	1998-01-20	San Miguel, Calle 10 #678	78901234	laura.morales@novabistro.com	4	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
1	1234567	Carlos	Mendoza	Silva	1985-03-15	Av. América #123, La Paz	70123456	carlos.mendoza@novabistro.com	1	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
11	235678	pedro	almodobar	Guzmán	1990-05-15	Av. Bush, Edificio Los Pinos, Apto 4B	70655443	pedro.almodobar@novabistro.com	2	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
2	2345678	María	Torres	Gutiérrez	1988-07-22	Calle 21 de Calacoto #456	71234567	maria.torres@novabistro.com	2	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
3	3456789	Juan	Pérez	López	\N	Zona Sur, Calle 15 #789	72345678	juan.perez@novabistro.com	2	t	$2b$12$cDtyuoPoH3UQ8owgeWxqT.R5AgdDW0lCb3mHVKg3WiAm2578abC36
12	1122334	adrian	davalos	pereira	\N	ormachea 2102	75146654	davalos@gmail.com	1	t	$2b$12$Wjg9tqoIuIP5IOn..KxS9ecGB1yqsCn5m6Td65VGFGleoj9aKKc7S
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.productos (id_producto, nombre, descripcion, precio_bs, id_categoria, disponible, activo) FROM stdin;
1	Anticucho de Corazón	Brochetas de corazón de res marinado, acompañado de papa y ají	35.00	1	t	t
2	Empanadas de Queso	Empanadas fritas rellenas de queso (3 unidades)	18.00	1	t	t
3	Salteñas	Empanadas horneadas tradicionales de carne o pollo (2 unidades)	16.00	1	t	t
4	Api con Pastel	Bebida caliente de maíz morado con pastel de queso	12.00	1	t	t
5	Huminta	Pasta de choclo envuelta en hojas (2 unidades)	14.00	1	t	t
6	Chairo Paceño	Sopa tradicional paceña con carne, chuño y verduras	25.00	2	t	t
7	Fricasé	Sopa picante de cerdo con mote y chuño	30.00	2	t	t
8	Sopa de Maní	Crema de maní con papas fritas y carne	28.00	2	t	t
9	Ají de Fideo	Sopa picante de fideos con papa y carne	26.00	2	t	t
10	Crema de Zapallo	Crema suave de zapallo con crutones	22.00	2	t	t
11	Pique Macho	Plato abundante de carne, salchicha, papas fritas, cebolla y locoto	45.00	3	t	t
13	Sajta de Pollo	Pollo deshilachado en salsa de ají amarillo con chuño phuti	35.00	3	t	t
14	Chicharrón de Cerdo	Chicharrón crocante con mote, chuño y llajua	42.00	3	t	t
15	Trucha a la Plancha	Trucha fresca del lago con ensalada y papas	48.00	3	t	t
16	Lechón al Horno	Cerdo horneado con salsa especial y guarniciones	55.00	3	t	t
17	Parrillada Personal	Chorizo, costilla, pollo y carne con papas y ensalada	65.00	4	t	t
18	Parrillada Familiar	Parrillada para 4 personas con variedad de carnes	220.00	4	t	t
19	Costillas BBQ	Costillas de cerdo con salsa barbacoa (500g)	58.00	4	t	t
20	Chuleta de Cerdo	Chuleta a la parrilla con papas y vegetales	48.00	4	t	t
21	Quinua a la Jardinera	Quinua con verduras salteadas y especias	32.00	5	t	t
22	Ensalada NovaBistro	Ensalada mixta con aguacate, queso y aderezo especial	28.00	5	t	t
23	Lasaña Vegetariana	Lasaña con verduras y salsa bechamel	38.00	5	t	t
24	Risotto de Hongos	Arroz cremoso con hongos y queso parmesano	42.00	5	t	t
25	Helado de Canela	Helado artesanal de canela (2 bolas)	18.00	6	t	t
26	Flan Casero	Flan tradicional con caramelo	15.00	6	t	t
27	Mousse de Chocolate	Mousse cremoso de chocolate belga	22.00	6	t	t
28	Torta de Zanahoria	Porción de torta casera de zanahoria	20.00	6	t	t
29	Helado de Tres Sabores	Helado artesanal de chocolate, vainilla y fresa	20.00	6	t	t
30	Café Americano	Café negro preparado en cafetera	12.00	7	t	t
31	Café Cortado	Café con un toque de leche	13.00	7	t	t
32	Cappuccino	Café con leche espumosa y canela	18.00	7	t	t
33	Té de Hierbas	Té de manzanilla, menta o anís	10.00	7	t	t
34	Chocolate Caliente	Chocolate espeso con leche	15.00	7	t	t
35	Jugo Natural	Jugo de frutas frescas (papaya, piña, frutilla, tumbo)	15.00	8	t	t
36	Limonada Frozen	Limonada granizada con menta	16.00	8	t	t
37	Refresco en Botella	Coca-Cola, Sprite, Fanta (500ml)	8.00	8	t	t
38	Agua Mineral	Agua sin gas (500ml)	6.00	8	t	t
39	Chicha Morada	Bebida de maíz morado con frutas	12.00	8	t	t
40	Mojito Sin Alcohol	Menta, lima, azúcar y soda	22.00	9	t	t
41	Piña Colada Virgin	Piña, coco y crema	25.00	9	t	t
42	Frutilla Daiquiri	Frutillas frescas con hielo frappe	24.00	9	t	t
43	Cóctel Tropical	Mix de frutas tropicales	26.00	9	t	t
12	Sillpancho Especial	Version familiar con doble huevo	42.00	2	t	t
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (id_rol, nombre, descripcion, activo) FROM stdin;
1	Administrador	Acceso total al sistema, gestión completa del restaurante	t
2	Mesero	Personal de atención al cliente, toma de pedidos	t
3	Cocinero	Personal de cocina, preparación de alimentos	t
4	Cajero	Personal de caja, facturación y cobros	t
\.


--
-- Name: categorias_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categorias_id_categoria_seq', 9, true);


--
-- Name: detalle_pedidos_id_detalle_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalle_pedidos_id_detalle_seq', 60, true);


--
-- Name: mesas_id_mesa_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mesas_id_mesa_seq', 20, true);


--
-- Name: pedidos_id_pedido_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pedidos_id_pedido_seq', 24, true);


--
-- Name: personal_id_personal_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.personal_id_personal_seq', 12, true);


--
-- Name: productos_id_producto_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.productos_id_producto_seq', 43, true);


--
-- Name: roles_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.roles_id_rol_seq', 5, true);


--
-- Name: categorias categorias_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_nombre_key UNIQUE (nombre);


--
-- Name: categorias categorias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categorias
    ADD CONSTRAINT categorias_pkey PRIMARY KEY (id_categoria);


--
-- Name: detalle_pedidos detalle_pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_pedidos
    ADD CONSTRAINT detalle_pedidos_pkey PRIMARY KEY (id_detalle);


--
-- Name: mesas mesas_numero_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mesas
    ADD CONSTRAINT mesas_numero_key UNIQUE (numero);


--
-- Name: mesas mesas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mesas
    ADD CONSTRAINT mesas_pkey PRIMARY KEY (id_mesa);


--
-- Name: pedidos pedidos_numero_pedido_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_numero_pedido_key UNIQUE (numero_pedido);


--
-- Name: pedidos pedidos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_pkey PRIMARY KEY (id_pedido);


--
-- Name: personal personal_ci_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personal
    ADD CONSTRAINT personal_ci_key UNIQUE (ci);


--
-- Name: personal personal_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personal
    ADD CONSTRAINT personal_email_key UNIQUE (email);


--
-- Name: personal personal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personal
    ADD CONSTRAINT personal_pkey PRIMARY KEY (id_personal);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id_producto);


--
-- Name: roles roles_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_nombre_key UNIQUE (nombre);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_rol);


--
-- Name: idx_detalle_pedido; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_detalle_pedido ON public.detalle_pedidos USING btree (id_pedido);


--
-- Name: idx_pedidos_estado; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pedidos_estado ON public.pedidos USING btree (estado);


--
-- Name: idx_pedidos_mesa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pedidos_mesa ON public.pedidos USING btree (id_mesa);


--
-- Name: idx_personal_rol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_personal_rol ON public.personal USING btree (id_rol);


--
-- Name: idx_productos_categoria; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_productos_categoria ON public.productos USING btree (id_categoria);


--
-- Name: detalle_pedidos detalle_pedidos_id_pedido_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_pedidos
    ADD CONSTRAINT detalle_pedidos_id_pedido_fkey FOREIGN KEY (id_pedido) REFERENCES public.pedidos(id_pedido) ON DELETE CASCADE;


--
-- Name: detalle_pedidos detalle_pedidos_id_producto_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_pedidos
    ADD CONSTRAINT detalle_pedidos_id_producto_fkey FOREIGN KEY (id_producto) REFERENCES public.productos(id_producto);


--
-- Name: pedidos pedidos_id_mesa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_id_mesa_fkey FOREIGN KEY (id_mesa) REFERENCES public.mesas(id_mesa);


--
-- Name: pedidos pedidos_id_personal_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos
    ADD CONSTRAINT pedidos_id_personal_fkey FOREIGN KEY (id_personal) REFERENCES public.personal(id_personal);


--
-- Name: personal personal_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personal
    ADD CONSTRAINT personal_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.roles(id_rol);


--
-- Name: productos productos_id_categoria_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_id_categoria_fkey FOREIGN KEY (id_categoria) REFERENCES public.categorias(id_categoria);


--
-- PostgreSQL database dump complete
--

\unrestrict WQ2EI8msZcp4AtzeF67wkitquoBwM5lJEwnQ6vsf80HOobJUmPaeFJnaffJbECs

