from datetime import datetime
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="TPV Ramírez - Esmeralda Minimal", page_icon="💡", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0b110e; color: #d4f0df; }
    .card-top { background: #122218; border: 1px solid #1e3f2b; padding: 20px; border-radius: 14px; margin-bottom: 20px; }
    .stButton>button { background-color: #173824; color: #00ffaa; border: 1px solid #00ffaa; border-radius: 8px; font-weight: bold; width: 100%; height: 45px; }
    .stButton>button:hover { background-color: #00ffaa; color: #0b110e; }
    </style>
""",
    unsafe_allow_html=True,
)

DATABASE = "ramirez_definitivo.db"


def get_db():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn


if "carrito" not in st.session_state:
  st.session_state.carrito = []

st.markdown(
    """
    <div class="card-top">
        <h1 style='color: #00ffaa; margin:0; font-size: 24px;'>🌿 TPV MULTI SERVICIOS RAMIREZ</h1>
        <p style='color: #7ab895; margin:5px 0 0 0;'>Modo: Esmeralda Minimalista | Dependiente: RAFELIN MENDEZ</p>
    </div>
""",
    unsafe_allow_html=True,
)

conn = get_db()
prods = conn.execute("SELECT codigo, nombre FROM productos").fetchall()
conn.close()
opciones = [f"{p['codigo']} - {p['nombre']}" for p in prods]

c1, c2, c3 = st.columns([3, 1, 1])
with c1:
  sel = st.selectbox(
      "Seleccionar Artículo:", ["-- Buscar producto --"] + opciones
  )
with c2:
  uni = st.number_input("Cant.", value=1.0, min_value=0.1)
with c3:
  st.write("")
  st.write("")
  if st.button("Añadir") and sel != "-- Buscar producto --":
    cod = sel.split(" - ")[0]
    conn = get_db()
    p = conn.execute(
        "SELECT * FROM productos WHERE codigo = ?", (cod,)
    ).fetchone()
    conn.close()
    if p:
      st.session_state.carrito.append({
          "codigo": p["codigo"],
          "nombre": p["nombre"],
          "unids": uni,
          "precio_base": p["precio_base"],
          "iva": p["iva"],
      })
      st.rerun()

st.markdown("### 🛒 Resumen de Venta")
if st.session_state.carrito:
  tot = sum(
      i["unids"] * i["precio_base"] * (1 + i["iva"] / 100)
      for i in st.session_state.carrito
  )
  for idx, i in enumerate(st.session_state.carrito):
    st.text(
        f"{i['nombre']} x {i['unids']} —"
        f" {(i['unids']*i['precio_base']*(1+i['iva']/100)):.2f} €"
    )
  st.markdown(f"## Total a Pagar: {tot:.2f} €")
  if st.button("✅ Cobrar Venta"):
    st.success("¡Cobrado con éxito!")
    st.session_state.carrito = []
    st.rerun()
else:
  st.info("El carrito está vacío.")
