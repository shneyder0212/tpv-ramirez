from datetime import datetime
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Multi Servicios Ramirez - TPV Profesional",
    page_icon="🟢",
    layout="wide",
)

# --- ESTILO VISUAL MODERNO Y VERDECITO DE ALTA GAMA ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1410;
        color: #e2f0e6;
        font-family: 'Segoe UI', sans-serif;
    }
    .top-banner {
        background: linear-gradient(135deg, #132a1c 0%, #08110b 100%);
        border: 1px solid #1e422a;
        border-radius: 12px;
        padding: 18px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 255, 128, 0.08);
    }
    .panel-caja {
        background: #111e15;
        border: 1px solid #1a3824;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
    .total-display {
        background: linear-gradient(145deg, #0f2418 0%, #07120c 100%);
        border: 2px solid #00ff88;
        border-radius: 12px;
        padding: 20px;
        text-align: right;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.15);
    }
    .stButton>button {
        background-color: #1b472b;
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 8px;
        font-weight: 700;
        height: 48px;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #00ff88;
        color: #0d1410;
        box-shadow: 0 0 12px rgba(0,255,136,0.4);
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

if "carrito" not in st.session_state:
  st.session_state.carrito = []

# --- CABECERA ---
st.markdown(
    """
    <div class="top-banner">
        <div>
            <h2 style='color: #00ff88; margin: 0;'>🌿 MULTI SERVICIOS RAMIREZ</h2>
            <p style='color: #9cbda7; margin: 2px 0 0 0; font-size: 13px;'>Terminal TPV Principal • Interfaz Verde Ejecutiva</p>
        </div>
        <div style='text-align: right;'>
            <span style='background: #194228; color: #00ff88; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 12px; border: 1px solid #00ff88;'>EN LÍNEA</span>
            <p style='color: #9cbda7; margin: 4px 0 0 0; font-size: 12px;'>Cajero: <b>RAFELIN MENDEZ</b></p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- CARGAR PRODUCTOS ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT codigo, nombre FROM productos")
lista_prods = cursor.fetchall()
conn.close()

opciones_map = {f"{p['codigo']} — {p['nombre']}": p["codigo"] for p in lista_prods}

# --- SECCIÓN DE ENTRADA RÁPIDA ---
st.markdown('<div class="panel-caja">', unsafe_allow_html=True)
col_sel, col_cant, col_btn = st.columns([3, 1, 1])

with col_sel:
  elegido = st.selectbox(
      "🔍 Seleccionar o buscar artículo en inventario:",
      options=["-- Seleccionar producto --"] + list(opciones_map.keys()),
  )

with col_cant:
  cant = st.number_input("Unidades", min_value=0.1, value=1.0, step=1.0)

with col_btn:
  st.write("")
  st.write("")
  agregar = st.button("➕ Añadir", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if agregar and elegido != "-- Seleccionar producto --":
  cod_sel = opciones_map[elegido]
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM productos WHERE codigo = ?", (cod_sel,))
  prod_data = cursor.fetchone()
  conn.close()

  if prod_data:
    st.session_state.carrito.append({
        "codigo": prod_data["codigo"],
        "nombre": prod_data["nombre"],
        "unids": cant,
        "precio_base": prod_data["precio_base"],
        "iva": prod_data["iva"],
    })
    st.rerun()

# --- CUERPO PRINCIPAL: TICKET Y TOTALES ---
col_izq, col_der = st.columns([2, 1])

with col_izq:
  st.markdown('<div class="panel-caja">', unsafe_allow_html=True)
  st.subheader("📋 Artículos en el Ticket")

  if st.session_state.carrito:
    for idx, item in enumerate(st.session_state.carrito):
      b = item["unids"] * item["precio_base"]
      cuota = b * (item["iva"] / 100)
      tot_lin = b + cuota

      c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
      c1.write(f"**{item['nombre']}**\n\n`{item['codigo']}`")
      c2.write(f"{item['unids']} u.")
      c3.write(f"{item['precio_base']:.2f} €")
      c4.write(f"**{tot_lin:.2f} €**")
      st.markdown(
          "<hr style='margin: 6px 0; border-color: #193823;'>",
          unsafe_allow_html=True,
      )

    st.write("")
    b1, b2, b3 = st.columns(3)
    if b1.button("🗑️ Vaciar Ticket", use_container_width=True):
      st.session_state.carrito = []
      st.rerun()
    if b2.button("🖨️ Imprimir Ticket", use_container_width=True):
      st.info("Imprimiendo ticket...")
    if b3.button("📂 Abrir Caja", use_container_width=True):
      st.success("Caja abierta.")
  else:
    st.info("El ticket está vacío. Selecciona un producto arriba.")

  st.markdown("</div>", unsafe_allow_html=True)

with col_der:
  st.markdown('<div class="total-display">', unsafe_allow_html=True)
  st.markdown(
      "<h4 style='color: #00ff88; margin: 0 0 10px 0;'>RESUMEN DE VENTA</h4>",
      unsafe_allow_html=True,
  )

  base_t = sum(i["unids"] * i["precio_base"] for i in st.session_state.carrito)
  iva_t = sum(
      (i["unids"] * i["precio_base"]) * (i["iva"] / 100)
      for i in st.session_state.carrito
  )
  total_g = base_t + iva_t

  st.markdown(
      f"<p style='margin: 4px 0; color: #a4c7b0; font-size: 14px;'>Base:"
      f" <b>{base_t:.2f} €</b></p>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<p style='margin: 4px 0; color: #a4c7b0; font-size: 14px;'>IVA:"
      f" <b>{iva_t:.2f} €</b></p>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<h2 style='color: #00ff88; margin: 12px 0; font-size: 28px;'>TOTAL:"
      f" {total_g:.2f} €</h2>",
      unsafe_allow_html=True,
  )

  if st.button("✅ COBRAR (F5)", use_container_width=True):
    if st.session_state.carrito:
      st.success("¡Venta cobrada correctamente!")
      st.session_state.carrito = []
      st.rerun()
    else:
      st.warning("El carrito está vacío.")

  st.markdown("</div>", unsafe_allow_html=True)
