const URL = 'http://localhost:8000';
let usuario = null, pedido_actual = [], mesa_seleccionada = null, todos_los_productos = [], lista_personal_local = [], lista_categorias_local = [];
const roles_nom = { 1: 'ADMINISTRADOR', 2: 'MESERO', 3: 'COCINA', 4: 'CAJERO' }, categorias_maestras = {};

async function login() {
    const ci = document.getElementById('login-ci').value, pass = document.getElementById('login-pass').value;
    if (!ci || !pass) return alert("Ingrese credenciales");
    try {
        const res = await fetch(`${URL}/personal/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ci: parseInt(ci), password: pass }) });
        if (res.ok) {
            usuario = await res.json();
            document.getElementById('login-vista').style.display = 'none';
            document.getElementById('app-vista').style.display = 'flex';
            document.getElementById('txt-nombre-usuario').innerText = usuario.nombre;
            configurarMenu();
        } else { document.getElementById('error-login').classList.remove('hidden'); }
    } catch (e) { alert("Error de conexión"); }
}

function configurarMenu() {
    const nav = document.getElementById('menu-navegacion'); nav.innerHTML = '';
    if (usuario.id_rol == 1) {
        nav.innerHTML += `<button onclick="irA('admin')" class="hover:text-amber-500 cursor-pointer">DASHBOARD</button>`;
        nav.innerHTML += `<button onclick="irA('reportes')" class="hover:text-amber-500 cursor-pointer">REPORTES</button>`;
    }
    nav.innerHTML += `<button onclick="irA('mesero')" class="hover:text-amber-500 cursor-pointer">SALÓN</button>`;
    if (usuario.id_rol == 1 || usuario.id_rol == 3) nav.innerHTML += `<button onclick="irA('cocina')" class="hover:text-amber-500 cursor-pointer">COCINA</button>`;
    if (usuario.id_rol == 1 || usuario.id_rol == 4) nav.innerHTML += `<button onclick="irA('caja')" class="hover:text-amber-500 cursor-pointer">CAJA</button>`;
    irA(usuario.id_rol == 1 ? 'admin' : usuario.id_rol == 2 ? 'mesero' : usuario.id_rol == 3 ? 'cocina' : 'caja');
}

function irA(s) {
    document.querySelectorAll('.seccion').forEach(x => x.style.display = 'none');
    document.getElementById(`panel-${s}`).style.display = 'block';
    if (s == 'admin') cargarAdmin(); if (s == 'mesero') cargarMesero(); if (s == 'cocina') cargarCocina(); if (s == 'caja') cargarCaja(); if (s == 'reportes') cargarReportes();
}

async function cargarAdmin() {
    const p = document.getElementById('panel-admin');
    p.innerHTML = `<div id="cards-resumen" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8"></div>
        <div class="panel-oscuro p-6 shadow-xl mb-8 border border-neutral-800">
            <div class="flex justify-between items-center mb-6 border-b border-neutral-800 pb-4"><h3 class="font-black text-amber-600 uppercase text-xs">Personal</h3><button onclick="abrirFormPersonal()" class="bg-emerald-800 px-4 py-2 rounded text-[10px] font-black uppercase">+ Nuevo</button></div>
            <div class="overflow-x-auto"><table class="w-full text-left text-xs min-w-[1000px]"><thead class="bg-neutral-900 text-neutral-500 uppercase font-black"><tr><th class="p-4 border-r border-neutral-800">C.I.</th><th class="p-4 border-r border-neutral-800">Nombre</th><th class="p-4 border-r border-neutral-800">Paterno</th><th class="p-4 border-r border-neutral-800">Materno</th><th class="p-4 border-r border-neutral-800">Teléfono</th><th class="p-4 border-r border-neutral-800">Rol</th><th class="p-4 text-center">Acciones</th></tr></thead><tbody id="lista-personal"></tbody></table></div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="panel-oscuro p-6 border border-neutral-800"><div class="flex justify-between items-center mb-4"><h3 class="font-black text-amber-600 uppercase text-xs">Categorías</h3><button onclick="abrirFormCategoria()" class="bg-emerald-800 px-3 py-1 rounded text-[9px] font-black uppercase">+ Nueva</button></div><table class="w-full text-xs text-left"><tbody id="lista-categorias-admin"></tbody></table></div>
            <div class="panel-oscuro p-6 border border-neutral-800"><div class="flex justify-between items-center mb-4"><h3 class="font-black text-amber-600 uppercase text-xs">Productos</h3><button onclick="abrirFormProducto()" class="bg-emerald-800 px-3 py-1 rounded text-[9px] font-black uppercase">+ Nuevo</button></div><table class="w-full text-xs text-left"><tbody id="lista-productos"></tbody></table></div>
        </div>`;
    const resC = await fetch(`${URL}/categorias/`); lista_categorias_local = await resC.json(); 
    const lC = document.getElementById('lista-categorias-admin');
    lista_categorias_local.forEach(c => { categorias_maestras[c.id_categoria] = c.nombre; lC.innerHTML += `<tr class="border-b border-neutral-800 text-xs"><td class="p-3 uppercase font-bold text-white">${c.nombre}</td><td class="p-3 text-center flex gap-2 justify-center"><button class="bg-blue-900 text-white text-[9px] px-2 py-1 rounded font-black uppercase" onclick="abrirFormCategoria(${c.id_categoria})">Edit</button><button class="bg-red-900 text-white text-[9px] px-2 py-1 rounded font-black uppercase" onclick="borrar('categorias', ${c.id_categoria})">Baja</button></td></tr>`; });
    const resRep = await fetch(`${URL}/reportes/general`); const r = await resRep.json();
    document.getElementById('cards-resumen').innerHTML = `<div class="panel-oscuro p-6 border-l-4 border-amber-600 text-center shadow-xl"><p class="text-[9px] uppercase text-neutral-500 mb-1">Ventas Brutas Totales</p><p class="text-3xl font-black text-white">Bs. ${parseFloat(r.resumen_general.total_ventas_bs || 0).toFixed(2)}</p></div><div class="panel-oscuro p-6 border-l-4 border-neutral-600 text-center shadow-xl"><p class="text-[9px] uppercase text-neutral-500 mb-1">Servicios Finalizados</p><p class="text-3xl font-black text-white">${r.resumen_general.total_pedidos || 0}</p></div>`;
    const resP = await fetch(`${URL}/personal/`); lista_personal_local = await resP.json();
    const lP = document.getElementById('lista-personal');
    lista_personal_local.forEach(p => { lP.innerHTML += `<tr class="hover:bg-neutral-800/50 text-xs border-b border-neutral-800 text-center"><td class="p-4 font-black text-amber-600">${p.ci}</td><td class="p-4 text-white uppercase font-bold text-left">${p.nombre}</td><td class="p-4 uppercase text-left">${p.apellido_paterno}</td><td class="p-4 uppercase text-left">${p.apellido_materno || '-'}</td><td class="p-4 font-mono">${p.telefono || '-'}</td><td class="p-4 text-[8px] font-black uppercase">${roles_nom[p.id_rol]}</td><td class="p-4 text-center"><button class="bg-blue-900/50 text-blue-400 border border-blue-800 text-[9px] px-3 py-1 rounded font-black" onclick="abrirFormPersonal(${p.id_personal})">Editar</button></td></tr>`; });
    const resPr = await fetch(`${URL}/productos/`); todos_los_productos = await resPr.json();
    const lPr = document.getElementById('lista-productos'); let ag = {};
    todos_los_productos.forEach(x => { let cn = categorias_maestras[x.id_categoria] || 'General'; if(!ag[cn]) ag[cn] = []; ag[cn].push(x); });
    for(let cat in ag) {
        lPr.innerHTML += `<tr class="bg-neutral-900"><td colspan="3" class="p-2 text-[9px] font-black text-amber-700 uppercase border-y border-neutral-800 text-center tracking-widest">${cat}</td></tr>`;
        ag[cat].forEach(x => { lPr.innerHTML += `<tr class="border-b border-neutral-800 text-xs hover:bg-neutral-800/50"><td class="p-3 uppercase font-bold text-neutral-300 text-left">${x.nombre}</td><td class="p-3 text-amber-500 font-black">Bs. ${parseFloat(x.precio_bs).toFixed(2)}</td><td class="p-3 text-center"><button class="bg-blue-900 text-white text-[9px] px-2 py-1 rounded font-black uppercase" onclick="abrirFormProducto(${x.id_producto})">Edit</button></td></tr>`; });
    }
}

async function cargarMesero() {
    const res = await fetch(`${URL}/mesas/`); const ms = await res.json(); const g = document.getElementById('grilla-mesas'); g.innerHTML = '';
    ms.forEach(m => {
        const c = m.estado == 'disponible' ? 'bg-neutral-900 border-emerald-900 text-emerald-500' : 'bg-red-900/30 border-red-800 text-red-500 shadow-xl';
        g.innerHTML += `<div onclick='seleccionarMesa(${JSON.stringify(m)})' class='p-5 border-2 rounded-xl text-center cursor-pointer font-black transition-all hover:scale-105 shadow-xl ${c}'>MESA ${m.numero}<br><span class="text-[8px] opacity-50 uppercase tracking-widest">${m.capacidad} PAX</span></div>`;
    });
}

async function seleccionarMesa(m) {
    mesa_seleccionada = m;
    const vO = document.getElementById('vista-detalle-ocupada'), vL = document.getElementById('vista-menu-libre'), pC = document.getElementById('panel-carrito-registro'), divC = document.getElementById('cont-categorias-salon'), areaS = document.getElementById('contenedor-salon');
    areaS.classList.remove('hidden'); document.getElementById('titulo-mesa').innerText = 'DETALLE MESA ' + m.numero;
    vO.classList.add('hidden'); vL.classList.add('hidden'); pC.classList.add('hidden'); divC.innerHTML = '';
    if (m.estado != 'disponible') {
        vO.classList.remove('hidden');
        try {
            const resA = await fetch(`${URL}/pedidos/mesa/${m.id_mesa}/activo`), d = await resA.json();
            if (d && d.detalles) {
                document.getElementById('contenido-detalle-json').innerHTML = d.detalles.map(it => `<div class="border-b border-neutral-800 pb-2 flex justify-between"><div><p class="text-[11px] font-bold text-neutral-300 uppercase">${it.cantidad}x ${it.producto}</p>${it.observaciones ? `<p class="text-[9px] text-amber-500 italic mt-1 italic">"${it.observaciones}"</p>` : ''}</div><span class="text-amber-600 font-mono text-xs">Bs. ${parseFloat(it.subtotal_bs).toFixed(2)}</span></div>`).join('');
                document.getElementById('txt-total-roja').innerText = 'Bs. ' + parseFloat(d.pedido.total_bs).toFixed(2);
            } else {
                document.getElementById('contenido-detalle-json').innerHTML = `<div class="py-20 text-center text-neutral-600 font-black uppercase text-[10px] tracking-widest italic opacity-50 text-center">Mesa ocupada sin pedido activo vinculado</div>`;
                document.getElementById('txt-total-roja').innerText = 'Bs. 0.00';
            }
        } catch (e) { document.getElementById('contenido-detalle-json').innerHTML = `<div class="py-20 text-center text-red-900 font-black uppercase text-[10px]">Error al consultar pedido</div>`; }
        return;
    }
    if (usuario.id_rol == 3) return;
    vL.classList.remove('hidden'); if (usuario.id_rol == 1 || usuario.id_rol == 2) pC.classList.remove('hidden');
    pedido_actual = []; dibujarCarrito();
    const resCats = await fetch(`${URL}/categorias/`); const cats = await resCats.json();
    const resPrs = await fetch(`${URL}/productos/`); todos_los_productos = await resPrs.json();
    divC.innerHTML = `<button onclick="dibujarProductos(null, this)" class="btn-cat bg-amber-600 text-white text-[9px] px-3 py-1 rounded font-black uppercase tracking-tighter transition-all">Todos</button>`;
    cats.forEach(c => { divC.innerHTML += `<button onclick="dibujarProductos(${c.id_categoria}, this)" class="btn-cat bg-neutral-900 text-amber-600 border border-neutral-700 text-[9px] px-3 py-1 rounded font-black uppercase hover:border-amber-600 transition-all">${c.nombre}</button>`; });
    dibujarProductos();
}

function dibujarProductos(idCat = null, el = null) {
    const btns = document.querySelectorAll('.btn-cat'); btns.forEach(b => { b.classList.remove('bg-amber-600', 'text-white'); b.classList.add('bg-neutral-900', 'text-amber-600'); });
    if(el) { el.classList.remove('bg-neutral-900', 'text-amber-600'); el.classList.add('bg-amber-600', 'text-white'); } else if(btns.length > 0) { btns[0].classList.remove('bg-neutral-900', 'text-amber-600'); btns[0].classList.add('bg-amber-600', 'text-white'); }
    const div = document.getElementById('items-menu'); div.innerHTML = '';
    const filtrados = idCat ? todos_los_productos.filter(p => p.id_categoria == idCat) : todos_los_productos;
    filtrados.forEach(p => { div.innerHTML += `<div onclick='agregar(${JSON.stringify(p)})' class='p-4 bg-neutral-900 border border-neutral-800 rounded-lg cursor-pointer hover:border-amber-600 transition-all uppercase font-black text-[9px] shadow-lg text-center h-full flex flex-col justify-between'><p class="text-neutral-400 mb-2 leading-tight">${p.nombre}</p><p class="text-amber-600 text-xs font-mono">Bs. ${parseFloat(p.precio_bs).toFixed(2)}</p></div>`; });
}

function agregar(p) {
    const ex = pedido_actual.find(x => x.id_producto == p.id_producto);
    if (ex) ex.cantidad++; else pedido_actual.push({ id_producto: p.id_producto, nombre: p.nombre, precio: p.precio_bs, cantidad: 1, observaciones: "" });
    dibujarCarrito();
}

function cambiarCant(i, delta) { pedido_actual[i].cantidad += delta; if (pedido_actual[i].cantidad <= 0) quitar(i); else dibujarCarrito(); }
function agregarNota(i) { const n = prompt("Nota:", pedido_actual[i].observaciones); if (n !== null) { pedido_actual[i].observaciones = n; dibujarCarrito(); } }
function quitar(i) { pedido_actual.splice(i, 1); dibujarCarrito(); }

function dibujarCarrito() {
    const div = document.getElementById('carrito'); div.innerHTML = ''; let t = 0;
    if(pedido_actual.length === 0) { div.innerHTML = `<p class="text-center text-[10px] py-16 italic opacity-50 text-neutral-600 uppercase font-black">Pulse platos del menú</p>`; document.getElementById('total-bs').innerText = '0.00'; return; }
    pedido_actual.forEach((it, i) => {
        t += parseFloat(it.precio) * it.cantidad;
        div.innerHTML += `<div class="bg-neutral-900/50 p-3 rounded border border-neutral-800 shadow-xl border-l-2 border-amber-600"><div class="flex justify-between font-black text-white text-[10px] uppercase mb-3"><span>${it.nombre}</span><span class="text-amber-600">Bs. ${(it.precio * it.cantidad).toFixed(2)}</span></div><div class="flex justify-between items-center"><button onclick="agregarNota(${i})" class="boton-nota text-[8px] uppercase font-black text-neutral-500">Nota</button><div class="flex gap-2 items-center"><button onclick="cambiarCant(${i}, -1)" class="boton-cantidad">-</button><span class="text-white font-black w-5 text-center text-xs">${it.cantidad}</span><button onclick="cambiarCant(${i}, 1)" class="boton-cantidad">+</button><button onclick="quitar(${i})" class="boton-eliminar ml-2 text-[10px] hover:bg-red-800 transition-colors uppercase">×</button></div></div></div>`;
    });
    document.getElementById('total-bs').innerText = t.toFixed(2);
}

async function enviarPedido() {
    if(!mesa_seleccionada) return alert("Seleccione mesa"); if(pedido_actual.length == 0) return alert("Vacio");
    const p = { id_mesa: mesa_seleccionada.id_mesa, id_personal: usuario.id_personal, detalles: pedido_actual };
    await fetch(`${URL}/pedidos/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) });
    await fetch(`${URL}/mesas/${mesa_seleccionada.id_mesa}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ numero: mesa_seleccionada.numero, capacidad: mesa_seleccionada.capacidad, ubicacion: mesa_seleccionada.ubicacion, estado: 'ocupada' }) });
    alert("¡Orden enviada!"); pedido_actual = []; mesa_seleccionada = null; irA('mesero');
}

async function cargarCocina() {
    const res = await fetch(`${URL}/pedidos/estado/pendiente`); const peds = await res.json(); const d = document.getElementById('lista-cocina'); d.innerHTML = '';
    for(let p of peds) { 
        const resD = await fetch(`${URL}/pedidos/detalle/${p.id_pedido}`); const data = await resD.json();
        d.innerHTML += `<div class="panel-oscuro p-5 border-l-4 border-amber-600 shadow-xl"><div class="flex justify-between mb-4 uppercase font-black text-amber-600 text-xs tracking-widest"><p>${p.numero_pedido}</p><span class="bg-neutral-800 px-2 py-1 rounded text-[8px]">Mesa ${p.id_mesa}</span></div><div class="space-y-3 mb-6 border-y border-neutral-800/50 py-4">${data.detalles.map(it => `<div class="text-[11px] uppercase font-bold text-neutral-300 leading-tight">- ${it.cantidad}x ${it.producto}${it.observaciones ? `<br><span class="text-[9px] text-amber-500/80 italic ml-3 font-medium">Nota: ${it.observaciones}</span>` : ''}</div>`).join('')}</div><button onclick="completar(${p.id_pedido})" class="w-full p-3 bg-emerald-900/30 text-emerald-500 border border-emerald-800 font-black text-[10px] rounded uppercase tracking-widest hover:bg-emerald-800 hover:text-white transition-all">Hecho</button></div>`; 
    }
}

async function completar(id) { await fetch(`${URL}/pedidos/${id}/estado?estado=completado`, { method: 'PUT' }); cargarCocina(); }

async function cargarCaja() {
    const res = await fetch(`${URL}/pedidos/estado/completado`); const peds = await res.json(); const d = document.getElementById('lista-caja'); d.innerHTML = '';
    peds.forEach(p => { d.innerHTML += `<div class="panel-oscuro p-6 text-center border border-neutral-800 transition-transform hover:scale-105 shadow-2xl"><p class="text-amber-600 text-[10px] font-black uppercase tracking-widest mb-2">${p.numero_pedido}</p><p class="text-3xl font-black text-white my-4 tracking-tighter font-mono">Bs. ${parseFloat(p.total_bs).toFixed(2)}</p><button onclick="imprimir(${p.id_pedido}, ${p.id_mesa})" class="w-full p-3 bg-amber-700 hover:bg-amber-600 text-white font-black text-[10px] rounded uppercase tracking-widest shadow-lg">Cobrar</button></div>`; });
}

async function imprimir(id, nm) {
    const res = await fetch(`${URL}/reportes/individual/pedido/${id}`); const d = await res.json(); const rep = d.reporte_pedido;
    let htmlTicket = `<div style="font-family: 'Courier New', Courier, monospace; color: black; background: white; padding: 30px; border: 1px solid #000; max-width: 400px; margin: auto;">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="margin: 0; font-size: 22px;">NOVABISTRO</h2>
            <p style="margin: 5px 0; font-size: 12px; font-weight: bold;">*** RECIBO DE PAGO ***</p>
        </div>
        <div style="font-size: 11px; margin-bottom: 15px;">
            <p style="margin: 2px 0;"><b>TICKET:</b> ${rep.numero_pedido}</p>
            <p style="margin: 2px 0;"><b>FECHA:</b> ${new Date(rep.fecha).toLocaleString()}</p>
            <p style="margin: 2px 0;"><b>MESA:</b> ${rep.mesa} | <b>ATENDIÓ:</b> ${rep.mesero}</p>
        </div>
        <table style="width: 100%; font-size: 11px; border-collapse: collapse; border-top: 1px dashed #000; border-bottom: 1px dashed #000; margin-bottom: 15px;">
            <thead><tr><th style="text-align: left; padding: 5px 0;">CANT.</th><th style="text-align: left;">PRODUCTO</th><th style="text-align: right;">BS.</th></tr></thead>
            <tbody>
                ${d.detalles.map(it => `<tr><td style="padding: 3px 0;">${it.cantidad}</td><td>${it.producto}</td><td style="text-align: right;">${parseFloat(it.subtotal).toFixed(2)}</td></tr>`).join('')}
            </tbody>
        </table>
        <div style="text-align: right; font-size: 16px; font-weight: bold;">
            TOTAL: Bs. ${parseFloat(rep.total_bs).toFixed(2)}
        </div>
        <div style="text-align: center; margin-top: 30px; font-size: 10px;">
            <p>¡GRACIAS POR SU PREFERENCIA!</p>
            <p>SANTACRUZ - BOLIVIA</p>
        </div>
    </div>`;
    document.getElementById('detalle-impresion').innerHTML = htmlTicket;
    await fetch(`${URL}/pedidos/${id}/estado?estado=entregado`, { method: 'PUT' });
    const resM = await fetch(`${URL}/mesas/`); const ms = await resM.json(); const m = ms.find(x => x.id_mesa == nm || x.numero == nm);
    if(m) await fetch(`${URL}/mesas/${m.id_mesa}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ numero: m.numero, capacidad: m.capacidad, ubicacion: m.ubicacion, estado: 'disponible' }) });
    window.print(); cargarCaja();
}

async function cargarReportes() {
    const resD = await fetch(`${URL}/reportes/diario`); const d = await resD.json(); const vHoy = parseFloat(d.resumen.total_ventas_bs || 0).toFixed(2);
    document.getElementById('cont-reporte-diario').innerHTML = `<div class="flex justify-between items-center bg-emerald-900/20 p-4 rounded border border-emerald-900/50 mb-4"><div><p class="text-3xl font-black text-white">Bs. ${vHoy}</p><p class="text-[9px] uppercase font-black text-emerald-500 tracking-widest">Hoy</p></div><div class="text-right"><p class="text-3xl font-black text-white">${d.resumen.total_pedidos || 0}</p><p class="text-[9px] uppercase font-black text-emerald-500 tracking-widest">Ventas</p></div></div><div class="space-y-2 max-h-[300px] overflow-y-auto text-xs">${d.pedidos_hoy.map(p => `<div class="flex justify-between bg-neutral-900 p-2 rounded border border-neutral-800 uppercase shadow-sm"><span>${p.numero_pedido}</span><span class="font-bold text-amber-500">Bs. ${parseFloat(p.total_bs).toFixed(2)}</span></div>`).join('')}</div>`;
    const resG = await fetch(`${URL}/reportes/general`); const g = await resG.json();
    const vHist = parseFloat(g.resumen_general.total_ventas_bs || 0).toFixed(2);
    let htmlG = `<div class="grid grid-cols-1 gap-4 mb-8"><div class="bg-neutral-900 p-4 rounded border border-neutral-800 text-center shadow-xl"><b>Bs. ${vHist}</b><br><span class="text-[8px] text-neutral-500 uppercase font-black tracking-widest uppercase">Ventas Brutas Históricas</span></div></div><div class="space-y-6 max-h-[400px] overflow-y-auto">`;
    let sag = {}; g.ventas_detalladas.forEach(v => { if(!sag[v.categoria]) sag[v.categoria] = []; sag[v.categoria].push(v); });
    for(let cat in sag) { htmlG += `<div class="bg-neutral-900/50 p-3 rounded border border-neutral-800"><p class="font-black text-amber-600 text-[9px] uppercase mb-3 border-b border-neutral-800 pb-1 tracking-widest">${cat}</p><div class="space-y-2">${sag[cat].map(p => `<div class="flex justify-between text-[10px] uppercase"><span>${p.unidades}x ${p.producto}</span><span class="text-white font-mono">Bs. ${parseFloat(p.subtotal).toFixed(2)}</span></div>`).join('')}</div></div>`; }
    document.getElementById('cont-reporte-general').innerHTML = htmlG + `</div>`;
    const sel = document.getElementById('sel-personal-reporte'); sel.innerHTML = '<option value="">Auditar empleado...</option>';
    lista_personal_local.forEach(p => { sel.innerHTML += `<option value="${p.id_personal}">${p.nombre} ${p.apellido_paterno}</option>`; });
}

async function generarReportePersonal() {
    const id = document.getElementById('sel-personal-reporte').value; if(!id) return;
    const res = await fetch(`${URL}/reportes/individual/personal/${id}`); const d = await res.json();
    const cont = document.getElementById('cont-reporte-individual'); cont.classList.remove('hidden');
    const vGen = parseFloat(d.estadisticas.total_generado_bs || 0).toFixed(2);
    cont.innerHTML = `<div class="flex justify-between items-center border-b border-neutral-800 pb-4 mb-4 uppercase"><h4 class="font-black text-white text-xs tracking-widest">${d.empleado.nombre} ${d.empleado.apellido_paterno}</h4><div class="text-right text-amber-500"><p class="text-xl font-black tracking-tighter">Bs. ${vGen}</p></div></div><p class="text-[9px] uppercase font-black text-neutral-500 mb-2 tracking-widest">Servicios Realizados</p><div class="grid grid-cols-1 md:grid-cols-2 gap-2">${d.ultimos_pedidos.map(p => `<div class="bg-neutral-900 p-2 rounded flex justify-between text-[10px] border border-neutral-800 uppercase shadow-sm"><span>${p.numero_pedido}</span><span class="font-bold">Bs. ${parseFloat(p.total_bs).toFixed(2)}</span></div>`).join('')}</div>`;
}

function abrirFormPersonal(id = null) {
    const d = id ? lista_personal_local.find(p => p.id_personal == id) : null;
    document.getElementById('modal-personal').style.display = 'flex';
    document.getElementById('form-titulo-p').innerText = d ? 'Actualizar Ficha' : 'Nuevo Personal';
    document.getElementById('p-ci').value = d ? d.ci : ''; document.getElementById('p-nombre').value = d ? d.nombre : '';
    document.getElementById('p-paterno').value = d ? d.apellido_paterno : ''; document.getElementById('p-materno').value = d ? (d.apellido_materno || '') : '';
    document.getElementById('p-tel').value = d ? (d.telefono || '') : ''; document.getElementById('p-email').value = d ? (d.email || '') : '';
    document.getElementById('p-dir').value = d ? (d.direccion || '') : ''; document.getElementById('p-rol').value = d ? d.id_rol : 1;
    document.getElementById('btn-guardar-p').onclick = () => guardarPersonal(id);
}

async function guardarPersonal(id) {
    const data = { ci: parseInt(document.getElementById('p-ci').value), nombre: document.getElementById('p-nombre').value, apellido_paterno: document.getElementById('p-paterno').value, apellido_materno: document.getElementById('p-materno').value, telefono: document.getElementById('p-tel').value, email: document.getElementById('p-email').value, direccion: document.getElementById('p-dir').value, id_rol: parseInt(document.getElementById('p-rol').value), password: '123456' };
    await fetch(id ? `${URL}/personal/${id}` : `${URL}/personal/`, { method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
    cerrarModal('personal'); cargarAdmin();
}

function abrirFormProducto(id = null) {
    const d = id ? todos_los_productos.find(p => p.id_producto == id) : null;
    document.getElementById('modal-producto').style.display = 'flex';
    const sel = document.getElementById('pr-cat'); sel.innerHTML = '';
    for (let cid in categorias_maestras) { sel.innerHTML += `<option value="${cid}" ${d && d.id_categoria == cid ? 'selected' : ''}>${categorias_maestras[cid]}</option>`; }
    document.getElementById('pr-nombre').value = d ? d.nombre : ''; document.getElementById('pr-precio').value = d ? d.precio_bs : '';
    document.getElementById('pr-desc').value = d ? (d.descripcion || '') : '';
    document.getElementById('btn-guardar-pr').onclick = () => guardarProducto(id);
}

async function guardarProducto(id) {
    const data = { nombre: document.getElementById('pr-nombre').value, precio_bs: parseFloat(document.getElementById('pr-precio').value), id_categoria: parseInt(document.getElementById('pr-cat').value), descripcion: document.getElementById('pr-desc').value };
    await fetch(id ? `${URL}/productos/${id}` : `${URL}/productos/`, { method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
    cerrarModal('producto'); cargarAdmin();
}

function abrirFormCategoria(id = null) {
    const d = id ? lista_categorias_local.find(c => c.id_categoria == id) : null;
    document.getElementById('modal-categoria').style.display = 'flex';
    document.getElementById('cat-nombre').value = d ? d.nombre : '';
    document.getElementById('btn-guardar-cat').onclick = () => guardarCategoria(id);
}

async function guardarCategoria(id) {
    const data = { nombre: document.getElementById('cat-nombre').value, descripcion: "" };
    await fetch(id ? `${URL}/categorias/${id}` : `${URL}/categorias/`, { method: id ? 'PUT' : 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
    cerrarModal('categoria'); cargarAdmin();
}

function cerrarModal(id) { document.getElementById(`modal-${id}`).style.display = 'none'; }
async function borrar(entidad, id) { if(confirm("¿Baja definitiva?")) { await fetch(`${URL}/${entidad}/${id}`, { method: 'DELETE' }); cargarAdmin(); } }
function salir() { location.reload(); }
