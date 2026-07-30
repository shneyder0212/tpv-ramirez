import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TPV - Multi Servicios Ramirez", page_icon="🛒", layout="centered"
)

st.title("🛒 TPV - Multi Servicios Ramirez")
st.markdown("---")

# Base de datos completa de alimentación con Precio de Compra y Precio de Venta directo
if "inventario" not in st.session_state:
  st.session_state.inventario = pd.DataFrame([
      {
          "codigo": "000000000001",
          "articulo": "SAZON LIQUIDO RANCHERO 400ML",
          "p_compra": 0.87,
          "p_venta": 2.47,
          "stock": 0.0,
      },
      {
          "codigo": "000000000002",
          "articulo": "GANDULES VERDES CON COCO GOYA",
          "p_compra": 2.11,
          "p_venta": 2.72,
          "stock": 6.0,
      },
      {
          "codigo": "000000000003",
          "articulo": "OREGANO RANCHERO EN POLVO 90GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 12.0,
      },
      {
          "codigo": "000000000004",
          "articulo": "FRIJOLES NEGROS PLEBEYO 400GR",
          "p_compra": 0.00,
          "p_venta": 2.06,
          "stock": 0.0,
      },
      {
          "codigo": "000000000005",
          "articulo": "SALSA DE AJI PICANTE 200ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
      },
      {
          "codigo": "000000000006",
          "articulo": "SAZON CRIOLLO BALDOM SIN PIMIENTA",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 7.0,
      },
      {
          "codigo": "000000000007",
          "articulo": "GUANDULES VERDES GOYA 425GR",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 28.0,
      },
      {
          "codigo": "000000000008",
          "articulo": "SAZON SUPER COMPLETO 283GR",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 0.0,
      },
      {
          "codigo": "000000000010",
          "articulo": "CABALLA EN SALSA DE TOMATE 425gr",
          "p_compra": 2.45,
          "p_venta": 3.30,
          "stock": 12.0,
      },
      {
          "codigo": "000000000011",
          "articulo": "AVENA EN HOJUELAS GOYA 500GR",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 14.0,
      },
      {
          "codigo": "000000000012",
          "articulo": "SALSA CHINA DE SOJA 200ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 2.0,
      },
      {
          "codigo": "000000000013",
          "articulo": "GUANDULES VERDES 822GR",
          "p_compra": 0.00,
          "p_venta": 3.14,
          "stock": -6.0,
      },
      {
          "codigo": "000000000014",
          "articulo": "LECHE DE COCO GOYA 500ML",
          "p_compra": 0.00,
          "p_venta": 2.47,
          "stock": 25.0,
      },
      {
          "codigo": "000000000020",
          "articulo": "COCA COLA LATA 330 ML",
          "p_compra": 0.61,
          "p_venta": 1.23,
          "stock": 61.0,
      },
      {
          "codigo": "000000000028",
          "articulo": "QUESO LATINO MI VAQUITA 30GR",
          "p_compra": 2.00,
          "p_venta": 2.72,
          "stock": 6.0,
      },
      {
          "codigo": "000000000029",
          "articulo": "AQUARIUS LIMON LATA 330ML",
          "p_compra": 0.62,
          "p_venta": 1.23,
          "stock": 31.0,
      },
      {
          "codigo": "000000000030",
          "articulo": "FANTA LATA 330ML",
          "p_compra": 0.49,
          "p_venta": 1.23,
          "stock": 36.0,
      },
      {
          "codigo": "000000000031",
          "articulo": "AGUA DE COCO GOYA LATA 350ML",
          "p_compra": 1.01,
          "p_venta": 1.23,
          "stock": 71.0,
      },
  ])

if "carrito" not in st.session_state:
  st.session_state.carrito = []

menu = st.sidebar.selectbox("Opciones", ["Caja / Venta", "Gestión de Artículos"])

if menu == "Caja / Venta":
  st.subheader("🛒 Cobro en Mostrador")

  busqueda = st.text_input("🔍 Buscar producto por nombre o código:").lower()

  df_inv = st.session_state.inventario
  if busqueda:
    df_inv = df_inv[
        df_inv["codigo"].str.lower().str.contains(busqueda)
        | df_inv["articulo"].str.lower().str.contains(busqueda)
    ]

  for index, row in df_inv.iterrows():
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
      st.write(f"**{row['articulo']}**")
      st.caption(f"Stock: {row['stock']} | Compra: {row['p_compra']:.2f} €")
    with col2:
      st.write(f"**P. Venta: {row['p_venta']:.2f} €**")
    with col3:
      if st.button("Añadir", key=f"add_{row['codigo']}"):
        st.session_state.carrito.append({
            "codigo": row["codigo"],
            "articulo": row["articulo"],
            "precio": row["p_venta"],
        })
        st.toast(f"Añadido: {row['articulo']}")

  st.markdown("---")
  st.subheader("🧾 Ticket Actual")

  if st.session_state.carrito:
    df_carrito = pd.DataFrame(st.session_state.carrito)
    st.dataframe(df_carrito[["articulo", "precio"]], use_container_width=True)

    total = df_carrito["precio"].sum()
    st.markdown(f"### Total a Pagar: **{total:.2f} €**")

    c1, c2 = st.columns(2)
    with c1:
      if st.button("✅ Cobrar"):
        st.success("¡Venta cobrada con éxito!")
        st.session_state.carrito = []
        st.rerun()
    with c2:
      if st.button("❌ Cancelar"):
        st.session_state.carrito = []
        st.rerun()
  else:
    st.info("El ticket está vacío.")

elif menu == "Gestión de Artículos":
  st.subheader("📦 Control de Precios (Compra y Venta) y Stock")

  st.dataframe(st.session_state.inventario, use_container_width=True)

  st.markdown("### Añadir Nuevo Producto")
  with st.form("form_nuevo"):
    ncod = st.text_input("Código")
    nart = st.text_input("Descripción del Producto")
    np_compra = st.number_input(
        "Precio de Compra (€)", min_value=0.0, value=0.0, step=0.01
    )
    np_venta = st.number_input(
        "Precio de Venta (€)", min_value=0.0, value=1.0, step=0.01
    )
    nstock = st.number_input("Existencias / Stock", value=0.0, step=1.0)

    submitted = st.form_submit_button("Guardar Artículo")
    if submitted and ncod and nart:
      nuevo = pd.DataFrame([{
          "codigo": ncod,
          "articulo": nart,
          "p_compra": np_compra,
          "p_venta": np_venta,
          "stock": nstock,
      }])
      st.session_state.inventario = pd.concat(
          [st.session_state.inventario, nuevo], ignore_index=True
      )
      st.success("¡Artículo guardado correctamente!")
      st.rerun()
