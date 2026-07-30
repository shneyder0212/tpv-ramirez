import sqlite3
from datetime import datetime
import streamlit as st

# Configuración de página en modo ancho para aprovechar toda la pantalla como un TPV real
st.set_page_config(page_title="Terminal Punto de Venta - Multi Servicios Ramirez", layout="wide")

# Estilos CSS personalizados para emular la interfaz de la foto (colores, paneles y estética de TPV clásico)
st.markdown("""
    <style>
    .main { background-color: #e6e6e6; }
    .tpv-header {
        background-color: #dcdcdc;
        border: 2px solid #b0b0b0;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .display-total {
        background-color: #000000;
        color: #00ffcc;
        font-size: 50px;
        font-weight: bold;
        text-align: right;
        padding: 15px;
        border: 4px solid #d97706;
        border-radius: 8px;
        font-family: monospace;
    }
    .panel-caja {
        background-color: #f0f0f0;
        border: 2px solid #c0c0c0;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

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

# Inicializar carrito de compras en sesión
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

conn = get_connection()
cursor = conn.cursor()

# --- CABECERA ESTILO TPV (Similar a la foto) ---
col_logo, col_info, col_visor = st.columns([2, 3, 3])

with col_logo:
    st.markdown("""
        <div style="border: 2px solid #d97706; padding: 10px; background: white; text-align: center; border-radius: 5px;">
            <h3 style="margin:0; color:#1e3a8a; font-size: 18px;">MULTI SERVICIOS RAMIREZ</h3>
            <p style="margin:0; font-size: 12px; color: gray;">Terminal Punto de Venta - León</p>
        </div>
    """, unsafe_allow_html=True)

with col_info:
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"""
        <div class="tpv-header">
            <span style="font-size: 13px;"><b>Serie de Ticket:</b> T1 (F11)</span><br>
            <span style="font-size: 13px;"><b>Fecha:</b> {fecha_hoy}</span><br>
            <span style="font-size: 13px;"><b>Dependiente:</b> 2 (F2) - <b>RAFELIN MENDEZ</b></span>
        </div>
    """, unsafe_allow_html=True)

# Cálculo dinámico del total actual del carrito con IVA incluido
total_calculado = sum(round(item['precio_base'] * item['cantidad'] * (1 + item['iva'] / 100.0), 2) for item in st.session_state.carrito)

with col_visor:
    st.markdown(f'<div class="display-total">{total_calculado:.2f}€</div>', unsafe_allow_html=True)

st.markdown("---")

# --- ZONA DE ENTRADA / LECTOR DE CÓDIGO DE BARRAS ---
col_input1, col_input2, col_input3 = st.columns([3, 1, 1])
codigo_o_busqueda = col_input1.text_input("🔍 Código de barras / Buscar artículo:", key="input_codigo", placeholder="Escanee con la pistola o escriba...")
cantidad_input = col_input2.number_input("Unidades", min_value=1.0, value=1.0, step=1.0)

if col_input3.button("Añadir (Enter)", type="primary"):
    if codigo_o_busqueda:
        cursor.execute("SELECT * FROM productos WHERE codigo = ? OR nombre LIKE ?", (codigo_o_busqueda, f"%{codigo_o_busqueda}%"))
        prod = cursor.fetchone()
        if prod:
            st.session_state.carrito.append({
                'codigo': prod['codigo'],
                'nombre': prod['nombre'],
                'precio_base': prod['precio_base'],
                'iva': float(prod['iva']),
                'cantidad': cantidad_input
            })
            st.rerun()
        else:
            st.error("Artículo no encontrado.")

# --- CUERPO PRINCIPAL: TABLA DE LÍNEAS DE TICKET ---
st.markdown("#### 📋 Líneas del Ticket")
header_cols = st.columns([2, 5, 1, 1, 1, 1])
header_cols[0].markdown("**Código**")
header_cols[1].markdown("**Descripción**")
header_cols[2].markdown("**Unids.**")
header_cols[3].markdown("**Precio**")
header_cols[4].markdown("**%IVA**")
header_cols[5].markdown("**Importe**")

st.markdown("<hr style='margin: 0px 0px 10px 0px;'>", unsafe_allow_html=True)

base_imponible_total = 0.0
iva_total = 0.0

for idx, item in enumerate(st.session_state.carrito):
    importe_con_iva = round(item['precio_base'] * item['cantidad'] * (1 + item['iva'] / 100.0), 2)
    imp_base_item = round(item['precio_base'] * item['cantidad'], 2)
    cuota_iva_item = round(imp_base_item * (item['iva'] / 100.0), 2)
    
    base_imponible_total += imp_base_item
    iva_total += cuota_iva_item
    
    row_cols = st.columns([2, 5, 1, 1, 1, 1])
    row_cols[0].text(item['codigo'])
    row_cols[1].text(item['nombre'])
    row_cols[2].text(str(item['cantidad']))
    row_cols[3].text(f"{item['precio_base']:.2f}€")
    row_cols[4].text(f"{item['iva']}%")
    row_cols[5].text(f"{importe_con_iva:.2f}€")

st.markdown("---")

# --- ZONA INFERIOR: BOTONES DE ACCIÓN RÁPIDA Y RESUMEN DE TOTALES ---
col_botones, col_resumen = st.columns([4, 3])

with col_botones:
    st.markdown("**Atajos de Teclado / Funciones:**")
    b1, b2, b3, b4 = st.columns(4)
    if b1.button("F5: Venta"):
        if st.session_state.carrito:
            st.success("¡Venta procesada con éxito!")
    if b2.button("F6: Cancelar"):
        st.session_state.carrito = []
        st.rerun()
    if b3.button("F7: Ticket"):
        st.info("Imprimiendo ticket de caja...")
    if b4.button("Esc: Cerrar"):
        st.warning("Sesión bloqueada.")

with col_resumen:
    st.markdown("""
        <div class="panel-caja">
    """, unsafe_allow_html=True)
    
    r1, r2 = st.columns(2)
    r1.text("Base imponible:")
    r2.text(f"{base_imponible_total:.2f} €")
    
    r1, r2 = st.columns(2)
    r1.text("IVA Total:")
    r2.text(f"{iva_total:.2f} €")
    
    r1, r2 = st.columns(2)
    r1.markdown("<b>TOTAL:</b>")
    r2.markdown(f"<b>{total_calculado:.2f} €</b>")
    
    st.markdown("</div>", unsafe_allow_html=True)

conn.close()
