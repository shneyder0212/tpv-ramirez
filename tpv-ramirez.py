from datetime import datetime
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="TPV Ramírez - CyberGreen", page_icon="⚡", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #050b07; color: #adffcf; }
    .cyber-panel { background: #0b1f13; border: 1px solid #00ff88; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,255,136,0.15); }
    .stButton>button { background-color: #00ff88; color: #050b07; font-weight: bold; border-radius: 6px; }
    .stButton>button:hover { background-color: #00cc6a; }
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
    <div class="cyber-panel">
        <h1 style='color: #00ff88; margin:0; text-shadow: 0 0 10px rgba(0,255,136,0.5);'>⚡ TPV MULTI SERVICIOS RAMIREZ</h1>
        <p style='color: #55aa82; margin:0;'>Cyber-Green System v3.0 | Operador: Rafelin Mendez</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.write("")
conn = get_db()
prods = conn.execute("SELECT codigo, nombre FROM productos").fetchall()
conn.close()
opciones = [f"{p['codigo']} - {p['nombre']}" for p in prods]

col1, col2 = st.columns([3, 1])
with col1:
  sel3 = st.selectbox(
      "BUSCADOR DE PRODUCTOS:", ["-- SELECCIONAR --"] + opciones
  )
  uni3 = st.number_input("CANTIDAD:", value=1.0, min_value=0.1)
  if st.button("⚡ AÑADIR AL TICKET"):
    if sel3 != "-- SELECCIONAR --":
      cod = sel3.split(" - ")[0]
      conn = get_db()
      p = conn.execute(
          "SELECT * FROM productos WHERE codigo = ?", (cod,)
      ).fetchone()
      conn.close()
      if p:
        st.session_state.carrito.append({
            "codigo": p["codigo"],
            "nombre": p["nombre"],
            "unids": uni3,
            "precio_base": p["precio_base"],
            "iva": p["iva"],
        })
        st.rerun()

with col2:
  tot3 = sum(
      i["unids"] * i["precio_base"] * (1 + i["iva"] / 100)
      for i in st.session_state.carrito
  )
  st.markdown(
      f"<div class='cyber-panel' style='text-align:center;'><h3>TOTAL</h3><h2"
      f" style='color:#00ff88;'>{tot3:.2f} €</h2></div>",
      unsafe_allow_html=True,
  )
  if st.button("💳 COBRAR"):
    st.success("¡Transacción Exitosa!")
    st.session_state.carrito = []
    st.rerun()

st.markdown("---")
st.write("### 📋 ÍTEMS SELECCIONADOS")
for item in st.session_state.carrito:
  st.code(
      f"{item['nombre']} | Cant: {item['unids']} | Total:"
      f" {(item['unids']*item['precio_base']*(1+item['iva']/100)):.2f} €"
  )
