from datetime import datetime
import sqlite3
import streamlit as st

st.set_page_config(
    page_title="TPV Ramírez - Bosque Profundo", page_icon="🌲", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0d1410; color: #e1edd7; }
    .forest-box { background: #152219; border-left: 5px solid #2ecc71; padding: 15px; border-radius: 4px; }
    .stButton>button { background-color: #27ae60; color: white; border-radius: 4px; font-weight: bold; }
    .stButton>button:hover { background-color: #219653; }
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
    <div class="forest-box">
        <h2 style='color: #2ecc71; margin:0;'>🌲 MULTI SERVICIOS RAMIREZ - BOSQUE PROFUNDO</h2>
        <p style='margin:0; color: #8fae96;'>Terminal Activa | Rafelin Mendez</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.write("")
conn = get_db()
prods = conn.execute("SELECT codigo, nombre FROM productos").fetchall()
conn.close()
opciones = [f"{p['codigo']} - {p['nombre']}" for p in prods]

colA, colB = st.columns([2, 1])
with colA:
  sel2 = st.selectbox(
      "Escáner / Producto:", ["-- Seleccionar producto --"] + opciones
  )
  uni2 = st.number_input("Unidades:", value=1.0, min_value=0.1)
  if st.button("➕ Agregar al Ticket"):
    if sel2 != "-- Seleccionar producto --":
      cod = sel2.split(" - ")[0]
      conn = get_db()
      p = conn.execute(
          "SELECT * FROM productos WHERE codigo = ?", (cod,)
      ).fetchone()
      conn.close()
      if p:
        st.session_state.carrito.append({
            "codigo": p["codigo"],
            "nombre": p["nombre"],
            "unids": uni2,
            "precio_base": p["precio_base"],
            "iva": p["iva"],
        })
        st.rerun()

with colB:
  st.markdown("### Caja Rápida")
  tot2 = sum(
      i["unids"] * i["precio_base"] * (1 + i["iva"] / 100)
      for i in st.session_state.carrito
  )
  st.metric("Total Acumulado", f"{tot2:.2f} €")
  if st.button("💳 Cobrar Ahora"):
    st.success("¡Cobro procesado!")
    st.session_state.carrito = []
    st.rerun()

st.markdown("---")
st.write("### Detalle del Ticket")
for idx, item in enumerate(st.session_state.carrito):
  st.write(
      f"• {item['nombre']} ({item['unids']} u.) —"
      f" {(item['unids']*item['precio_base']*(1+item['iva']/100)):.2f} €"
  )
