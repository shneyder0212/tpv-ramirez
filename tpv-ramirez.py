import sqlite3
from datetime import datetime
import streamlit as st

# Configuración de la página web
st.set_page_config(
    page_title="Multi Servicios Ramirez - TPV Profesional",
    page_icon="🛒",
    layout="wide"
)

DATABASE = 'ramirez_definitivo.db'

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
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 10.0, 1.80, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.0, 2.11, 2.72, 4),
            ('000000000003', 'OREGANO RANCHERO EN POLVO 90GR', 12.0, 1.90, 2.47, 10),
            ('000000000004', 'FRIJOLES NEGROS PLEBEYO 400GR', 8.0, 1.50, 2.06, 4),
            ('8410199026418', 'CERVEZA POKER 330ML', 24.0, 1.50, 2.06, 21),
            ('000000000006', 'AGUA VIVO 50ml', 15.0, 0.50, 1.00, 21),
            ('7702001001234', 'ARROZ DIANA BLANCO 1KG', 30.0, 1.10, 1.50, 4),
            ('7702002004567', 'ACEITE VEGETAL 1000CC', 10.0, 2.80, 3.75, 21),
            ('7702003007890', 'PAN TAJADO BIMBO', 12.0, 1.20, 1.65, 10),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

# Inicializar carrito en la sesión web
if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- CABECERA ---
st.markdown("""
    <div style='background-color: #1e1e1e; padding: 15px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center;'>
        <h3 style='color: white; margin: 0;'>🛒 M.S. RAMIREZ - Terminal Punto de Venta</h3>
        <p style='color: #00ffcc; margin: 0; font-weight: bold;'>Terminal: T1 | Dependiente: RAFELIN MENDEZ</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- PANEL DE BÚSQUEDA Y ACCIÓN ---
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    codigo_input = st.text_input("🔍 Escanee o escriba el código de barras / nombre del producto:", placeholder="Ej. 000000000006 o AGUA")

with col2:
    unidades = st.number_input("Unidades", min_value=0.1, value=1.0, step=1.0)

with col3:
    st.write("")
    st.write("")
    agregar_btn = st.button("➕ Añadir Producto", use_container_width=True)

# Lógica al añadir producto
if agregar_btn and codigo_input:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE codigo = ? OR nombre LIKE ?", (codigo_input.strip(), f"%{codigo_input.strip()}%"))
    prod = cursor.fetchone()
    conn.close()

    if prod:
        st.session_state.carrito.append({
            "codigo": prod["codigo"],
            "nombre": prod["nombre"],
            "unids": unidades,
            "precio_base": prod["precio_base"],
            "iva": prod["iva"]
        })
        st.success(f"Añadido: {prod['nombre']}")
        st.rerun()
    else:
        st.error("❌ Artículo no encontrado en la base de datos.")

st.markdown("---")

# --- TABLA DE LÍNEAS DEL TICKET ---
st.subheader("📋 Líneas del Ticket Actual")

if st.session_state.carrito:
    base_total = 0.0
    iva_total = 0.0
    
    # Mostrar tabla de productos en el carrito
    for i, item in enumerate(st.session_state.carrito):
        b = item["unids"] * item["precio_base"]
        cuota = b * (item["iva"] / 100)
        tot_lin = b + cuota
        
        base_total += b
        iva_total += cuota
        
        c1, c2, c3, c4, c5, c6 = st.columns([2, 4, 1, 1, 1, 1])
        c1.write(item["codigo"])
        c2.write(item["nombre"])
        c3.write(f"{item['unids']} u.")
        c4.write(f"{item['precio_base']:.2f} €")
        c5.write(f"{item['iva']}%")
        c6.write(f"**{tot_lin:.2f} €**")

    total_general = base_total + iva_total

    st.markdown("---")
    
    # --- TOTALES Y BOTONES DE COBRO ---
    col_tot1, col_tot2 = st.columns([2, 1])
    
    with col_tot1:
        b1, b2, b3 = st.columns(3)
        if b1.button("✅ Cobrar Venta (F5)", use_container_width=True):
            st.success("¡Venta cobrada y registrada con éxito!")
            st.session_state.carrito = []
            st.rerun()
        if b2.button("🗑️ Cancelar Ticket", use_container_width=True):
            st.session_state.carrito = []
            st.rerun()
        if b3.button("🖨️ Imprimir Ticket", use_container_width=True):
            st.info("Imprimiendo ticket...")

    with col_tot2:
        st.markdown(f"""
            <div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; text-align: right;'>
                <p style='margin: 0; color: #b0b0b0; font-size: 14px;'>Base Imponible: {base_total:.2f} €</p>
                <p style='margin: 0; color: #b0b0b0; font-size: 14px;'>IVA Total: {iva_total:.2f} €</p>
                <h2 style='margin: 0; color: #00ffcc;'>TOTAL: {total_general:.2f} €</h2>
            </div>
        """, unsafe_allow_html=True)

else:
    st.info("El carrito está vacío. Escanee un código o busque un producto arriba.")

# --- BARRA LATERAL PARA GESTIÓN DE INVENTARIO ---
with st.sidebar:
    st.header("⚙️ Gestión de Inventario")
    with st.form("form_nuevo"):
        st.subheader("Añadir / Editar Artículo")
        nuevo_cod = st.text_input("Código de Barras")
        nuevo_nom = st.text_input("Descripción")
        nuevo_costo = st.number_input("Costo (€)", value=0.0)
        nuevo_pvp = st.number_input("Precio Venta Base (€)", value=0.0)
        nuevo_iva = st.selectbox("IVA (%)", [21, 10, 4])
        
        guardar = st.form_submit_button("Guardar en BD")
        if guardar and nuevo_cod and nuevo_nom:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
                VALUES (?, ?, 0, ?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET
                nombre=excluded.nombre, costo_un=excluded.costo_un, precio_base=excluded.precio_base, iva=excluded.iva
            ''', (nuevo_cod, nuevo_nom.upper(), nuevo_costo, nuevo_pvp, nuevo_iva))
            conn.commit()
            conn.close()
            st.success("¡Artículo guardado con éxito!")
            st.rerun()

    st.markdown("---")
    st.write("📋 **Catálogo Actual en Base de Datos:**")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nombre, precio_base FROM productos")
    for row in cursor.fetchall():
        st.text(f"{row['codigo']} - {row['nombre'][:20]} ({row['precio_base']}€)")
    conn.close()
