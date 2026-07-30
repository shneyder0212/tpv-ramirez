from datetime import datetime
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="Multi Servicios Ramirez - TPV Master Edition",
    page_icon="✨",
    layout="wide",
)

# --- ESTILO VISUAL "MASTER EDITION" (VERDE ESMERALDA Y NEÓN) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #080d0a;
        color: #edf5f0;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    
    /* Tarjetas de diseño moderno */
    .master-card {
        background: linear-gradient(145deg, #111e16 0%, #0c140f 100%);
        border: 1px solid #1a3a24;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    
    /* Panel del total destacado */
    .checkout-box {
        background: linear-gradient(135deg, #102619 0%, #06110a 100%);
        border: 2px solid #00ff88;
        border-radius: 16px;
        padding: 24px;
        text-align: right;
        box-shadow: 0 0 25px rgba(0, 255, 136, 0.15);
    }

    /* Botones personalizados con estilo neón sutil */
    .stButton>button {
        background-color: #153b23;
        color: #00ff88;
        border: 1px solid #00ff88;
        border-radius: 10px;
        font-weight: 600;
        height: 50px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ff88;
        color: #080d0a;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
    }
    
    /* Estética de las tablas y selects */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #111e16;
        border-color: #1a3a24;
        border-radius: 10px;
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

# --- CABECERA PRINCIPAL ---
st.markdown(
    """
    <div class="master-card" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style='color: #00ff88; margin: 0; font-size: 26px; letter-spacing: 0.5px;'>🌿 MULTI SERVICIOS RAMIREZ</h1>
            <p style='color: #8fae9b; margin: 5px 0 0 0; font-size: 14px;'>Terminal Punto de Venta • Master Edition</p>
        </div>
        <div style='text-align: right;'>
            <span style='background: #153b23; color: #00ff88; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px; border: 1px solid #00ff88;'>● T1 - ACTIVO</span>
            <p style='color: #a0c4ae; margin: 5px 0 0 0; font-size: 12px;'>Operador: <b>RAFELIN MENDEZ</b></p>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- OBTENER PRODUCTOS PARA EL SELECTOR ---
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT codigo, nombre FROM productos")
catalogo_bd = cursor.fetchall()
conn.close()

opciones_productos = [
    f"{p['codigo']} — {p['nombre']}" for p in catalogo_bd
]

# --- ZONA DE OPERACIÓN (BUSCADOR Y ACCIÓN) ---
with st.container():
  st.markdown('<div class="master-card">', unsafe_allow_html=True)
  col_busq, col_unids, col_btn = st.columns([3,
