from datetime import datetime
import sqlite3
import streamlit as st

# Configuración de la página web
st.set_page_config(
    page_title="Multi Servicios Ramirez - TPV Profesional",
    page_icon="🛒",
    layout="wide",
)

# --- ESTILO VISUAL MODERNO CON TONOS VERDECITOS ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121814;
        color: #e0e0e0;
    }
    .header-box {
        background: linear-gradient(135deg, #1b3022 0%, #0f1c14 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2e5a3c;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,255,128,0.1);
    }
    .total-box {
        background: linear-gradient(135deg, #16261c 0%, #0a140e 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #00ff99;
        text-align: right;
        box-shadow: 0 4px 15px rgba(0,255,153,0.2);
    }
    .stButton>button {
        background-color: #1e462c;
        color: white;
        border: 1px solid #00ff99;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ff99;
        color: #121814;
    }
    </style>
""",
    unsafe_allow_html=True,
)

DATABASE = "ramirez_definitivo.db"


def get_connection():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            existencias REAL DEFAULT 0,
            costo_un REAL DEFAULT 0,
            precio_base REAL NOT NULL,
            iva INTEGER DEFAULT 21 CHECK(iva IN (21, 10, 4))
        )
    """
  )
  cursor.execute("SELECT COUNT(*) FROM productos")
  if cursor.fetchone()[0] == 0:
    productos_iniciales = [
        (
            "000000000001",
            "SAZON LIQUIDO RANCHERO 400ML",
            10.0,
            1.80,
            2.47,
            21,
        ),
        ("000000000002", "GANDULES VERDES CON COCO GOYA", 6.0, 2.11, 2.72, 4),
        ("000000000003", "OREGANO RANCHERO EN POLVO 90GR", 12.0, 1.90, 2.47, 10),
        ("000000000004", "FRIJOLES NEGROS PLEBEYO 400GR", 8.0, 1.50, 2.06, 4),
        ("8410199026418", "CERVEZA POKER 330ML", 24.0, 1.50, 2.06, 21),
        ("000000000006", "AGUA VIVO 50ml", 15.0, 0.50, 1.00, 21),
        ("7702001001234", "ARROZ DIANA BLANCO 1KG", 30.0, 1.10, 1.50, 4),
        ("7702002004567", "ACEITE VEGETAL 1000CC", 10.0, 2.80, 3.75, 21),
        ("7702003007890", "PAN TAJADO BIMBO", 12.0, 1.20, 1.65, 10),
    ]
    cursor.executemany(
        """
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        productos_iniciales,
    )
    conn.commit()
  conn.close()


init_db()

# Inicializar carrito
if "carrito" not in st.session_state:
  st.session_state.carrito = []

# --- CABECERA ESTILIZADA ---
st.markdown(
    """
    <div class="header-box">
        <h2 style='color: #00ff99; margin: 0;'>🛒 MULTI SERVICIOS RAMIREZ</h2>
        <p style='color: #a3ffcb; margin: 0; font-weight: bold;'>Terminal: T1 | Dependiente: RAFELIN MENDEZ</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.write("")

# --- OBTENER LISTA DE PRODUCTOS PARA AUTOCOMPLETADO INTELIGENTE ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT codigo, nombre FROM productos")
catalogo_bd = cursor.fetchall()
conn.close()

opciones_productos = [
    f"{p['codigo']} - {p['nombre']}" for p in catalogo_bd
]

# --- PANEL DE BÚSQUEDA Y SELECCIÓN ---
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
  seleccion_prod = st.selectbox(
      "🔍 Buscador Inteligente (Escriba o escanee código/nombre):",
      options=["-- Seleccione o busque un producto --"] + opciones_productos,
  )

with col2:
  unidades = st.number_input(
      "Unidades", min_value=0.1, value=1.0, step=1.0, format="%.1f"
  )

with col3:
  st.write("")
  st.write("")
  agregar_btn = st.button("➕ Añadir Producto", use_container_width=True)

if agregar_btn and seleccion_prod != "-- Seleccione o busque un producto --":
  codigo_encontrado = seleccion_prod.split(" - ")[0]

  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(
      "SELECT * FROM productos WHERE codigo = ?", (codigo_encontrado,)
  )
  prod = cursor.fetchone()
  conn.close()

  if prod:
    st.session_state.carrito.append({
        "codigo": prod["codigo"],
        "nombre": prod["nombre"],
        "unids": unidades,
        "precio_base": prod["precio_base"],
        "iva": prod["iva"],
    })
    st.success(f"¡Añadido con éxito: {prod['nombre']}!")
    st.rerun()

st.markdown("---")

# --- TABLA DE LÍNEAS DEL TICKET ACTUAL ---
st.subheader("📋 Líneas del Ticket Actual")

if st.session_state.carrito:
  base_total = 0.0
  iva_total = 0.0

  header_cols = st.columns([2, 4, 1, 1, 1, 1])
  header_cols[0].markdown("**Código**")
  header_cols[1].markdown("**Descripción**")
  header_cols[2].markdown("**Unids**")
  header_cols[3].markdown("**P. Base**")
  header_cols[4].markdown("**IVA**")
  header_cols[5].markdown("**Total**")

  st.markdown(
      "<hr style='margin:5px 0; border-color:#2e5a3c;'>", unsafe_allow_html=True
  )

  for i, item in enumerate(st.session_state.carrito):
    b = item["unids"] * item["precio_base"]
    cuota = b * (item["iva"] / 100)
    tot_lin = b + cuota

    base_total += b
    iva_total += cuota

    c1, c2, c3, c4, c5, c6 = st.columns([2, 4, 1, 1, 1, 1])
    c1.text(item["codigo"])
    c2.text(item["nombre"])
    c3.text(f"{item['unids']} u.")
    c4.text(f"{item['precio_base']:.2f} €")
    c5.text(f"{item['iva']}%")
    c6.text(f"{tot_lin:.2f} €")

  total_general = base_total + iva_total

  st.markdown("---")

  col_acciones, col_totales = st.columns([2, 1])

  with col_acciones:
    st.write("### Opciones de Caja")
    b1, b2, b3 = st.columns(3)
    if b1.button("✅ Cobrar Venta (F5)", use_container_width=True):
      st.success("¡Venta cobrada con éxito! Ticket registrado.")
      st.session_state.carrito = []
      st.rerun()
    if b2.button("🗑️ Cancelar Ticket", use_container_width=True):
      st.session_state.carrito = []
      st.rerun()
    if b3.button("🖨️ Imprimir Ticket", use_container_width=True):
      st.info("🖨️ Enviando ticket a la impresora física...")

  with col_totales:
    st.markdown(
        f"""
        <div class="total-box">
            <p style='margin: 0; color: #a3ffcb; font-size: 14px;'>Base Imponible: {base_total:.2f} €</p>
            <p style='margin: 0; color: #a3ffcb; font-size: 14px;'>IVA Total: {iva_total:.2f} €</p>
            <h2 style='margin: 5px 0 0 0; color: #00ff99;'>TOTAL: {total_general:.2f} €</h2>
        </div>
    """,
        unsafe_allow_html=True,
    )

else:
  st.info(
      "🛒 El carrito está vacío. Utiliza el buscador superior para añadir"
      " productos."
  )

# --- BARRA LATERAL: CONFIGURACIÓN Y GESTIÓN DE PRECIOS ---
with st.sidebar:
  st.header("⚙️ Configuración de Precios")
  st.markdown(
      "Modifica o añade los precios de compra, venta e IVA de cualquier"
      " artículo."
  )

  with st.form("form_configuracion_precio"):
    codigo_conf = st.text_input("Código de Barras del Producto")
    nombre_conf = st.text_input("Nombre / Descripción")
    costo_conf = st.number_input("Precio de Compra (Costo €)", value=0.0)
    pvp_conf = st.number_input("Precio de Venta Base (€)", value=0.0)
    iva_conf = st.selectbox("Tipo de IVA (%)", [21, 10, 4])

    guardar_conf = st.form_submit_button("💾 Guardar / Actualizar Precios")

    if guardar_conf and codigo_conf and nombre_conf:
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute(
          """
                INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
                VALUES (?, ?, 0, ?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET
                nombre=excluded.nombre, 
                costo_un=excluded.costo_un, 
                precio_base=excluded.precio_base, 
                iva=excluded.iva
            """,
          (
              codigo_conf,
              nombre_conf.upper(),
              costo_conf,
              pvp_conf,
              iva_conf,
          ),
      )
      conn.commit()
      conn.close()
      st.success("¡Configuración guardada correctamente!")
      st.rerun()

  st.markdown("---")
  st.subheader("📦 Catálogo y Costos en BD")
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(
      "SELECT codigo, nombre, costo_un, precio_base, iva FROM productos"
  )
  for r in cursor.fetchall():
    st.text(
        f"[{r['codigo']}]\n{r['nombre'][:25]}\nCosto: {r['costo_un']}€ | Venta:"
        f" {r['precio_base']}€ | IVA: {r['iva']}%"
    )
    st.markdown("---")
  conn.close()
