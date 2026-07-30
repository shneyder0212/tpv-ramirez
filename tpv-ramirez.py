import sqlite3
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# Configuración de página en modo ancho total
st.set_page_config(page_title="Terminal Punto de Venta - Multi Servicios Ramirez", layout="wide")

DATABASE = 'tienda.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            existencias REAL DEFAULT 0,
            costo_un REAL DEFAULT 0,
            precio_base REAL NOT NULL,
            iva INTEGER DEFAULT 21 CHECK(iva IN (21, 10, 4))
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 0.00, 0.00, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.00, 2.11, 2.72, 4),
            ('000000000003', 'OREGANO RANCHERO EN POLVO 90GR', 12.00, 0.00, 2.47, 10),
            ('000000000004', 'FRIJOLES NEGROS PLEBEYO 400GR', 0.00, 0.00, 2.06, 4),
            ('8410199026418', 'CERVEZA POKER 330ML', 10.00, 1.50, 2.06, 21),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

# Cargar productos de la base de datos para pasarlos al componente visual
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM productos")
rows = cursor.fetchall()
productos_json = []
for r in rows:
    productos_json.append({
        "codigo": r["codigo"],
        "nombre": r["nombre"],
        "precio_base": r["precio_base"],
        "iva": r["iva"]
    })
conn.close()

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

# Interfaz TPV Profesional exacta con HTML/CSS incrustado para eliminar el aspecto "feo" de Streamlit
tpv_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #f3f4f6; font-family: system-ui, -apple-system, sans-serif; }}
        .digital-screen {{
            background-color: #000;
            color: #00ffcc;
            font-family: monospace;
            text-shadow: 0 0 8px rgba(0,255,204,0.4);
        }}
        .tpv-border {{ border: 2px solid #d97706; }}
    </style>
</head>
<body class="p-4">
    <div class="max-w-7xl mx-auto space-y-4">
        
        <!-- CABECERA TPV -->
        <div class="grid grid-cols-12 gap-4 items-center">
            <!-- Logo / Info Negocio -->
            <div class="col-span-3 bg-white p-3 rounded tpv-border shadow-sm">
                <div class="flex items-center space-x-3">
                    <div class="bg-amber-600 text-white font-bold p-2 rounded text-xs text-center">TPV</div>
                    <div>
                        <h2 class="font-bold text-gray-800 text-sm">MULTI SERVICIOS RAMIREZ</h2>
                        <p class="text-xs text-gray-500">Terminal Punto de Venta - León</p>
                    </div>
                </div>
            </div>

            <!-- Datos de Sesión -->
            <div class="col-span-4 bg-gray-200 p-3 rounded border border-gray-300 text-xs space-y-1">
                <div><b>Serie de Ticket:</b> T1 (F11)</div>
                <div><b>Fecha:</b> {fecha_hoy}</div>
                <div><b>Dependiente:</b> 2 (F2) - <b>RAFELIN MENDEZ</b></div>
            </div>

            <!-- Visor Digital de Total -->
            <div class="col-span-5 digital-screen p-4 rounded-lg tpv-border text-right text-5xl font-bold tracking-wider" id="visor-total">
                0.00€
            </div>
        </div>

        <!-- ENTRADA Y LECTOR DE BARRAS -->
        <div class="bg-white p-3 rounded border border-gray-300 flex gap-4 items-center shadow-sm">
            <div class="flex-1">
                <label class="block text-xs font-bold text-gray-600 mb-1">CÓDIGO DE BARRAS / BUScar ARTÍCULO:</label>
                <input type="text" id="input-busqueda" placeholder="Escanee con la pistola o escriba..." 
                       class="w-full border border-gray-400 p-2 rounded text-sm focus:outline-none focus:border-amber-600" autofocus>
            </div>
            <div class="w-28">
                <label class="block text-xs font-bold text-gray-600 mb-1">UNIDADES:</label>
                <input type="number" id="input-unidades" value="1" min="1" 
                       class="w-full border border-gray-400 p-2 rounded text-sm text-center">
            </div>
            <div class="pt-5">
                <button onclick="agregarProducto()" class="bg-red-600 hover:bg-red-700 text-white font-bold px-5 py-2 rounded text-sm shadow">
                    Añadir (Enter)
                </button>
            </div>
        </div>

        <!-- CUERPO / TABLA DE LÍNEAS DE TICKET -->
        <div class="grid grid-cols-12 gap-4">
            <div class="col-span-8 bg-white rounded border border-gray-300 shadow-sm overflow-hidden flex flex-col" style="height: 380px;">
                <div class="bg-gray-100 border-b border-gray-300 grid grid-cols-12 p-2 text-xs font-bold text-gray-700">
                    <div class="col-span-3">Código</div>
                    <div class="col-span-5">Descripción</div>
                    <div class="col-span-1 text-center">Unids.</div>
                    <div class="col-span-1 text-right">Precio</div>
                    <div class="col-span-2 text-right">Importe</div>
                </div>
                <div id="lista-carrito" class="flex-1 overflow-y-auto divide-y divide-gray-100 text-xs">
                    <!-- Las líneas se cargan dinámicamente aquí -->
                </div>
            </div>

            <!-- PANEL LATERAL DE TOTALES Y ATAJOS -->
            <div class="col-span-4 space-y-4">
                <div class="bg-gray-100 p-4 rounded border border-gray-300 space-y-2 text-sm shadow-sm">
                    <div class="flex justify-between">
                        <span class="text-gray-600">Base imponible:</span>
                        <span id="lbl-base" class="font-mono font-bold">0.00 €</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-600">IVA Total:</span>
                        <span id="lbl-iva" class="font-mono font-bold">0.00 €</span>
                    </div>
                    <hr class="border-gray-300">
                    <div class="flex justify-between text-base">
                        <span class="font-bold text-gray-800">TOTAL:</span>
                        <span id="lbl-total-resumen" class="font-mono font-bold text-amber-700 text-lg">0.00 €</span>
                    </div>
                </div>

                <!-- Botones de Función estilo TPV -->
                <div class="bg-white p-3 rounded border border-gray-300 shadow-sm space-y-2">
                    <div class="text-xs font-bold text-gray-500 mb-1">Atajos de Teclado / Funciones:</div>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="procesarVenta()" class="bg-gray-200 hover:bg-gray-300 border border-gray-400 p-2 rounded text-xs font-bold text-gray-700">F5: Venta</button>
                        <button onclick="cancelarVenta()" class="bg-gray-200 hover:bg-gray-300 border border-gray-400 p-2 rounded text-xs font-bold text-gray-700">F6: Cancelar</button>
                        <button onclick="alert('Imprimiendo ticket...')" class="bg-gray-200 hover:bg-gray-300 border border-gray-400 p-2 rounded text-xs font-bold text-gray-700">F7: Ticket</button>
                        <button onclick="alert('Caja cerrada')" class="bg-gray-200 hover:bg-gray-300 border border-gray-400 p-2 rounded text-xs font-bold text-gray-700">Esc: Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const catalogo = {json.dumps(productos_json)};
        let carrito = [];

        document.getElementById('input-busqueda').addEventListener('keypress', function (e) {{
            if (e.key === 'Enter') {{
                agregarProducto();
            }}
        }});

        function agregarProducto() {{
            const input = document.getElementById('input-busqueda');
            const unidadesInput = document.getElementById('input-unidades');
            const query = input.value.trim().toLowerCase();
            const cantidad = parseFloat(unidadesInput.value) || 1;

            if (!query) return;

            const prod = catalogo.find(p => p.codigo === query || p.nombre.toLowerCase().includes(query));

            if (prod) {{
                const existente = carrito.find(item => item.codigo === prod.codigo);
                if (existente) {{
                    existente.cantidad += cantidad;
                }} else {{
                    carrito.push({{
                        codigo: prod.codigo,
                        nombre: prod.nombre,
                        precio_base: prod.precio_base,
                        iva: prod.iva,
                        cantidad: cantidad
                    }});
                }}
                input.value = '';
                unidadesInput.value = '1';
                input.focus();
                actualizarVista();
            }} else {{
                alert('Artículo no encontrado en el inventario.');
            }}
        }}

        function actualizarVista() {{
            const contenedor = document.getElementById('lista-carrito');
            contenedor.innerHTML = '';

            let baseImponibleTotal = 0;
            let ivaTotal = 0;
            let totalGeneral = 0;

            carrito.forEach((item, index) => {{
                const precioConIva = item.precio_base * (1 + item.iva / 100);
                const importeConIva = round(precioConIva * item.cantidad);
                const impBaseItem = round(item.precio_base * item.cantidad);
                const cuotaIvaItem = round(impBaseItem * (item.iva / 100));

                baseImponibleTotal += impBaseItem;
                ivaTotal += cuotaIvaItem;
                totalGeneral += importeConIva;

                const fila = document.createElement('div');
                fila.className = "grid grid-cols-12 p-2 items-center hover:bg-gray-50";
                fila.innerHTML = `
                    <div class="col-span-3 font-mono text-gray-600">${{item.codigo}}</div>
                    <div class="col-span-5 font-medium text-gray-800">${{item.nombre}}</div>
                    <div class="col-span-1 text-center font-bold">${{item.cantidad}}</div>
                    <div class="col-span-1 text-right">${{precioConIva.toFixed(2)}}€</div>
                    <div class="col-span-2 text-right font-bold">${{importeConIva.toFixed(2)}}€</div>
                `;
                contenedor.appendChild(fila);
            }});

            document.getElementById('visor-total').innerText = totalGeneral.toFixed(2) + '€';
            document.getElementById('lbl-base').innerText = baseImponibleTotal.toFixed(2) + ' €';
            document.getElementById('lbl-iva').innerText = ivaTotal.toFixed(2) + ' €';
            document.getElementById('lbl-total-resumen').innerText = totalGeneral.toFixed(2) + ' €';
        }}

        function cancelarVenta() {{
            carrito = [];
            actualizarVista();
        }}

        function procesarVenta() {{
            if (carrito.length === 0) {{
                alert('El carrito está vacío.');
                return;
            }}
            alert('¡Venta registrada y cobrada con éxito!');
            cancelarVenta();
        }}

        function round(value) {{
            return Math.round(value * 100) / 100;
        }}
    </script>
</body>
</html>
"""

# Renderizar el TPV con diseño profesional exacto dentro de Streamlit
components.html(tpv_html, height=650, scrolling=False)
