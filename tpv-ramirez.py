import sqlite3
import json
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

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
            ('000000000006', 'AGUA VIVO 50ml', 10.00, 0.50, 1.00, 21),
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 0.00, 0.00, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.00, 2.11, 2.72, 4),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM productos")
rows = cursor.fetchall()
productos_json = [{"codigo": r["codigo"], "nombre": r["nombre"], "precio_base": r["precio_base"], "iva": r["iva"]} for r in rows]
conn.close()

fecha_hoy = datetime.now().strftime("%d/%m/%Y")

tpv_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #dcdcdc; font-family: Tahoma, Arial, sans-serif; user-select: none; }}
        .tpv-panel {{ background-color: #ececec; border: 2px solid #b5651d; border-radius: 4px; box-shadow: inset 0 0 5px rgba(0,0,0,0.1); }}
        .digital-screen {{ background-color: #000; color: #00ffcc; font-family: 'Courier New', monospace; border: 3px solid #b5651d; text-shadow: 0 0 6px rgba(0,255,204,0.5); }}
        .tpv-grid-header {{ background-color: #d4d0c8; border-bottom: 2px solid #808080; font-weight: bold; color: #333; }}
        .tpv-row {{ border-bottom: 1px solid #d0d0d0; background-color: #ffffff; }}
        .tpv-row-active {{ background-color: #ffffd9; outline: 1px solid #0000ff; }}
        .btn-tpv {{ background: linear-gradient(to bottom, #f9f9f9, #e1e1e1); border: 1px solid #adadad; border-radius: 3px; font-weight: bold; color: #333; }}
        .btn-tpv:active {{ background: #dcdcdc; }}
    </style>
</head>
<body class="p-3">
    <div class="max-w-7xl mx-auto space-y-3">
        
        <!-- CABECERA SUPERIOR -->
        <div class="grid grid-cols-12 gap-3 items-center">
            <div class="col-span-3 tpv-panel p-2 bg-white flex items-center space-x-2">
                <div class="bg-amber-700 text-white font-bold p-2 text-xs rounded">TPV</div>
                <div>
                    <div class="font-bold text-xs text-gray-800">Terminal Punto de Venta</div>
                    <div class="text-[10px] text-gray-500">Terminal punto de venta y control de almacén</div>
                </div>
            </div>

            <div class="col-span-4 text-xs space-y-0.5 px-2">
                <div><b>Serie de Ticket:</b> T1 <span class="text-red-700 font-bold">F11</span></div>
                <div><b>Fecha:</b> {fecha_hoy}</div>
                <div><b>Dependiente:</b> 2 <span class="text-red-700 font-bold">F2</span> &nbsp;&nbsp; <b>RAFELIN MENDEZ</b></div>
            </div>

            <div class="col-span-5 digital-screen p-3 rounded text-right text-4xl font-bold tracking-widest" id="visor-total">
                0.00€
            </div>
        </div>

        <!-- CUADRO CENTRAL: TABLA TIPO EXCEL / TPV CLÁSICO -->
        <div class="tpv-panel p-2 bg-white">
            <div class="overflow-hidden border border-gray-400 bg-white" style="height: 320px;">
                <div class="grid grid-cols-12 tpv-grid-header p-1.5 text-xs">
                    <div class="col-span-3 px-1">Código</div>
                    <div class="col-span-5 px-1">Descripción</div>
                    <div class="col-span-1 text-center">Unids.</div>
                    <div class="col-span-1 text-right">Precio</div>
                    <div class="col-span-1 text-center">Desc.</div>
                    <div class="col-span-1 text-right">Importe</div>
                </div>
                
                <div id="cuerpo-tabla" class="overflow-y-auto text-xs" style="height: 275px;">
                    <!-- Fila activa de entrada -->
                    <div class="grid grid-cols-12 tpv-row tpv-row-active p-1 items-center">
                        <div class="col-span-3 px-1">
                            <input type="text" id="input-codigo" placeholder="Escribir o escanear..." 
                                   class="w-full bg-transparent focus:outline-none font-mono text-xs" autofocus>
                        </div>
                        <div class="col-span-5 px-1 text-gray-400 italic" id="preview-nombre">Seleccione producto...</div>
                        <div class="col-span-1 text-center"><input type="text" id="input-unids" value="1.00" class="w-full text-center bg-transparent focus:outline-none"></div>
                        <div class="col-span-1 text-right text-gray-400">0.00</div>
                        <div class="col-span-1 text-center text-gray-400">0.0</div>
                        <div class="col-span-1 text-right text-gray-400">0.00</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ZONA INFERIOR: BOTONES Y TOTALES -->
        <div class="grid grid-cols-12 gap-3 items-start">
            <!-- Botones de función -->
            <div class="col-span-7 grid grid-cols-4 gap-2 pt-1">
                <button onclick="alert('Acción Venta (F5)')" class="btn-tpv p-2 text-xs text-red-800"><b>F5</b> &nbsp; Venta</button>
                <button onclick="alert('Acción Ticket (F7)')" class="btn-tpv p-2 text-xs text-red-800"><b>F7</b> &nbsp; Ticket</button>
                <div class="col-span-2 flex items-center space-x-2 bg-white p-1.5 border border-gray-400 rounded">
                    <span class="text-xs text-red-800 font-bold">Descontar: Ctrl + F12</span>
                    <input type="text" value="0.00" class="w-16 text-right border border-gray-300 p-0.5 text-xs font-mono">
                </div>

                <button onclick="limpiarVenta()" class="btn-tpv p-2 text-xs text-red-800"><b>F6</b> &nbsp; Cancelar</button>
                <button onclick="alert('Caja (F8)')" class="btn-tpv p-2 text-xs text-red-800"><b>F8</b> &nbsp; Caja</button>
                <button onclick="alert('Cerrar')" class="btn-tpv p-2 text-xs text-red-800 col-span-2"><b>Esc</b> &nbsp; Cerrar</button>
            </div>

            <!-- Panel Derecho de Totales -->
            <div class="col-span-5 tpv-panel p-3 bg-white space-y-1.5 text-xs">
                <div class="flex justify-between items-center">
                    <span class="text-gray-700">Base imponible:</span>
                    <span id="lbl-base" class="font-mono font-bold bg-gray-100 px-2 py-0.5 border border-gray-300 w-28 text-right">0.00</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-700">IVA:</span>
                    <span id="lbl-iva" class="font-mono font-bold bg-gray-100 px-2 py-0.5 border border-gray-300 w-28 text-right">0.00</span>
                </div>
                <div class="flex justify-between items-center pt-1">
                    <span class="font-bold text-gray-900 text-sm">Total:</span>
                    <span id="lbl-total" class="font-mono font-bold text-sm bg-gray-100 px-2 py-1 border border-gray-300 w-28 text-right text-red-800">0.00</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        const catalogo = {json.dumps(productos_json)};
        let carrito = [];

        const inputCodigo = document.getElementById('input-codigo');
        const inputUnids = document.getElementById('input-unids');

        inputCodigo.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                const val = inputCodigo.value.trim();
                const unids = parseFloat(inputUnids.value) || 1.0;
                if (!val) return;

                const prod = catalogo.find(p => p.codigo === val || p.nombre.toLowerCase().includes(val.toLowerCase()));
                if (prod) {{
                    carrito.push({{
                        codigo: prod.codigo,
                        nombre: prod.nombre,
                        unidades: unids,
                        precio: prod.precio_base,
                        iva: prod.iva
                    }});
                    inputCodigo.value = '';
                    inputUnids.value = '1.00';
                    actualizarTabla();
                }} else {{
                    alert('Artículo no encontrado');
                }}
            }}
        }});

        function actualizarTabla() {{
            const cuerpo = document.getElementById('cuerpo-tabla');
            
            let htmlFilas = '';
            let baseImpTot = 0;
            let ivaTot = 0;
            let totalGen = 0;

            carrito.forEach(item => {{
                const importeBase = item.unidades * item.precio;
                const cuotaIva = importeBase * (item.iva / 100);
                const importeConIva = importeBase + cuotaIva;

                baseImpTot += importeBase;
                ivaTot += cuotaIva;
                totalGen += importeConIva;

                htmlFilas += `
                    <div class="grid grid-cols-12 tpv-row p-1 items-center">
                        <div class="col-span-3 px-1 font-mono">${{item.codigo}}</div>
                        <div class="col-span-5 px-1 font-medium">${{item.nombre}}</div>
                        <div class="col-span-1 text-center">${{item.unidades.toFixed(2)}}</div>
                        <div class="col-span-1 text-right">${{item.precio.toFixed(2)}}</div>
                        <div class="col-span-1 text-center">0.0</div>
                        <div class="col-span-1 text-right font-bold">${{importeConIva.toFixed(2)}}</div>
                    </div>
                `;
            }});

            // Mantener la fila de entrada activa al final
            htmlFilas += `
                <div class="grid grid-cols-12 tpv-row tpv-row-active p-1 items-center">
                    <div class="col-span-3 px-1">
                        <input type="text" id="input-codigo" placeholder="Escribir o escanear..." 
                               class="w-full bg-transparent focus:outline-none font-mono text-xs" autofocus>
                    </div>
                    <div class="col-span-5 px-1 text-gray-400 italic">Seleccione producto...</div>
                    <div class="col-span-1 text-center"><input type="text" id="input-unids" value="1.00" class="w-full text-center bg-transparent focus:outline-none"></div>
                    <div class="col-span-1 text-right text-gray-400">0.00</div>
                    <div class="col-span-1 text-center text-gray-400">0.0</div>
                    <div class="col-span-1 text-right text-gray-400">0.00</div>
                </div>
            `;

            cuerpo.innerHTML = htmlFilas;

            // Reasignar eventos al nuevo input creado
            const nuevoInput = document.getElementById('input-codigo');
            nuevoInput.focus();
            nuevoInput.addEventListener('keypress', arguments.callee);

            document.getElementById('visor-total').innerText = totalGen.toFixed(2) + '€';
            document.getElementById('lbl-base').innerText = baseImpTot.toFixed(2);
            document.getElementById('lbl-iva').innerText = ivaTot.toFixed(2);
            document.getElementById('lbl-total').innerText = totalGen.toFixed(2);
        }}

        function limpiarVenta() {{
            carrito = [];
            actualizarTabla();
        }}
    </script>
</body>
</html>
"""

components.html(tpv_html, height=580, scrolling=False)
