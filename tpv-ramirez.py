from datetime import datetime, date
import pandas as pd
import streamlit as st

# Configuración de página con diseño moderno y colores llamativos
st.set_page_config(
    page_title="TPV - Multi Servicios Ramirez", page_icon="⚡", layout="centered"
)

# Estilos CSS personalizados para darle un toque moderno, colorido y delicado
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        padding: 15px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar credenciales y datos en session_state
if "admin_nombre" not in st.session_state:
  st.session_state.admin_nombre = "Administrador"
if "empleado_nombre" not in st.session_state:
  st.session_state.empleado_nombre = "Empleado de Turno"
if "rol_activo" not in st.session_state:
  st.session_state.rol_activo = None

# Base de datos con inventario, precios y fecha de caducidad
if "inventario" not in st.session_state:
  st.session_state.inventario = pd.DataFrame([
      {
          "codigo": "000000000001",
          "articulo": "SAZON LIQUIDO RANCHERO 400ML",
          "p_compra": 0.87,
          "p_venta": 2.47,
          "stock": 10.0,
          "caducidad": "2027-06-15",
      },
      {
          "codigo": "000000000002",
          "articulo": "GANDULES VERDES CON COCO GOYA",
          "p_compra": 2.11,
          "p_venta": 2.72,
          "stock": 6.0,
          "caducidad": "2026-08-10",
      },
      {
          "codigo": "000000000020",
          "articulo": "COCA COLA LATA 330 ML",
          "p_compra": 0.61,
          "p_venta": 1.23,
          "stock": 61.0,
          "caducidad": "2026-06-01",
      },  # Ejemplo caducado para prueba
      {
          "codigo": "000000000028",
          "articulo": "QUESO LATINO MI VAQUITA 30GR",
          "p_compra": 2.00,
          "p_venta": 2.72,
          "stock": 6.0,
          "caducidad": "2026-07-15",
      },  # Ejemplo próximo a caducar
      {
          "codigo": "8410199026475",
          "articulo": "MONSTER ENERGY",
          "p_compra": 0.00,
          "p_venta": 1.65,
          "stock": 15.0,
          "caducidad": "2028-01-01",
      },
  ])

if "carrito" not in st.session_state:
  st.session_state.carrito = []

# --- PANTALLA DE ACCESO (LOGIN) ---
if st.session_state.rol_activo is None:
  st.markdown(
      "<h1"
      " style='text-align: center; color: #4f46e5;'>✨ Multi Servicios"
      " Ramirez ✨</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<h4 style='text-align: center; color: #6b7280;'>Sistema TPV Inteligente"
      " & Dinámico</h4>",
      unsafe_allow_html=True,
  )
  st.markdown("---")

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown("### 🔐 Iniciar Sesión")
    tipo_login = st.selectbox("Selecciona tu Rol:", ["Empleado", "Administrador"])
    clave = st.text_input("Clave de Acceso:", type="password")

    if st.button(
        "🚀 Acceder al Sistema", use_container_width=True, type="primary"
    ):
      if tipo_login == "Administrador" and clave == "admin123":
        st.session_state.rol_activo = "Administrador"
        st.success(
            f"¡Bienvenido, {st.session_state.admin_nombre} (Admin)!"
        )
        st.rerun()
      elif tipo_login == "Empleado" and clave == "emp123":
        st.session_state.rol_activo = "Empleado"
        st.success(f"¡Bienvenido, {st.session_state.empleado_nombre}!")
        st.rerun()
      else:
        st.error("❌ Clave incorrecta. Inténtalo de nuevo.")

else:
  # --- BARRA LATERAL MODERNA ---
  st.sidebar.markdown("### 🌟 Panel de Control")
  if st.session_state.rol_activo == "Administrador":
    st.sidebar.info(f"👑 **{st.session_state.admin_nombre}** (Admin)")
  else:
    st.sidebar.success(
        f"👤 **{st.session_state.empleado_nombre}** (Empleado)"
    )

  if st.sidebar.button(
      "🚪 Cerrar Sesión", use_container_width=True, type="secondary"
  ):
    st.session_state.rol_activo = None
    st.rerun()

  st.sidebar.markdown("---")
  opciones_menu = [
      "🛒 Caja / Venta",
      "📦 Gestión de Artículos",
      "⚠️ Alertas de Caducidad",
      "⚙️ Configuración Nombres",
  ]
  menu = st.sidebar.selectbox("Menú Principal", opciones_menu)

  # --- CAJA / VENTA ---
  if menu == "🛒 Caja / Venta":
    st.markdown(
        f"### ⚡ Caja Registradora Active | Turno: <b>"
        f"{st.session_state.empleado_nombre}</b>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    busqueda = st.text_input(
        "🔍 Buscar producto por nombre o código...", placeholder="Escribe aquí..."
    ).lower()

    df_inv = st.session_state.inventario
    if busqueda:
      df_inv = df_inv[
          df_inv["codigo"].str.lower().str.contains(busqueda)
          | df_inv["articulo"].str.lower().str.contains(busqueda)
      ]

    for index, row in df_inv.iterrows():
      with st.container():
        c1, c2, c3, c4 = st.columns([2.5, 1, 1, 1])
        with c1:
          st.write(f"**{row['articulo']}**")
          st.caption(f"Stock: {row['stock']} | Caducidad: {row['caducidad']}")
        with c2:
          st.markdown(f"**{row['p_venta']:.2f} €**")
        with c3:
          iva_sel = st.selectbox(
              "IVA",
              [21, 10, 4],
              key=f"iva_{row['codigo']}",
              label_visibility="collapsed",
          )
        with c4:
          if st.button("➕ Añadir", key=f"add_{row['codigo']}"):
            precio_con_iva = row["p_venta"] * (1 + iva_sel / 100.0)
            st.session_state.carrito.append({
                "codigo": row["codigo"],
                "articulo": f"{row['articulo']} (IVA {iva_sel}%)",
                "precio": precio_con_iva,
            })
            st.toast(f"✨ Añadido: {row['articulo']}")
      st.divider()

    # --- SECCIÓN DEL CARRITO Y FACTURACIÓN EMPRESA ---
    st.markdown("### 🧾 Ticket y Justificante para Empresa")

    if st.session_state.carrito:
      df_carrito = pd.DataFrame(st.session_state.carrito)
      st.dataframe(df_carrito[["articulo", "precio"]], use_container_width=True)

      total = df_carrito["precio"].sum()
      st.markdown(
          f"<h3 style='color: #4f46e5;'>Total a Pagar: {total:.2f} €</h3>",
          unsafe_allow_html=True,
      )

      # Opción de factura para reembolso de empresa
      with st.expander("🏢 Generar Justificante / Factura para Empresa"):
        st.markdown(
            "Introduce los datos del cliente que necesita el comprobante para"
            " su empresa:"
        )
        c_nombre = st.text_input("Nombre y Apellidos / Razón Social")
        c_nif = st.text_input("NIF / CIF de la Empresa")
        c_concepto = st.text_input("Concepto (ej. Dieta, Material Oficina)")

        if st.button("📄 Imprimir / Ver Justificante"):
          if c_nombre and c_nif:
            st.success(
                f"✅ Justificante generado correctamente para **{c_nombre}**"
                f" (NIF: {c_nif})"
            )
            st.markdown(f"""
                        > **MULTISERVICIOS RAMIREZ**
                        > -----------------------------------
                        > **Cliente:** {c_nombre}
                        > **NIF/CIF:** {c_nif}
                        > **Concepto:** {c_concepto or 'Compra habitual'}
                        > **Total Abonado:** {total:.2f} €
                        > **Atendido por:** {st.session_state.empleado_nombre}
                        > -----------------------------------
                        > *¡Gracias por su confianza!*
                        """)
          else:
            st.warning("⚠️ Por favor introduce al menos el Nombre y el NIF.")

      c1, c2 = st.columns(2)
      with c1:
        if st.button(
            "✅ Cobrar Venta", use_container_width=True, type="primary"
        ):
          st.balloons()
          st.success("🎉 ¡Venta cobrada con éxito!")
          st.session_state.carrito = []
          st.rerun()
      with c2:
        if st.button("❌ Cancelar", use_container_width=True):
          st.session_state.carrito = []
          st.rerun()
    else:
      st.info("🛒 El carrito está vacío. Selecciona productos arriba.")

  # --- GESTIÓN DE ARTÍCULOS ---
  elif menu == "📦 Gestión de Artículos":
    if st.session_state.rol_activo != "Administrador":
      st.warning(
          "⚠️ Zona exclusiva para el Administrador. Inicia sesión como Admin."
      )
    else:
      st.markdown("### 📦 Inventario y Control de Caducidades")
      st.dataframe(st.session_state.inventario, use_container_width=True)

      st.markdown("### ➕ Añadir Nuevo Producto con Caducidad")
      with st.form("form_nuevo"):
        ncod = st.text_input("Código de Barras")
        nart = st.text_input("Descripción del Producto")
        np_compra = st.number_input(
            "Precio de Compra (€)", min_value=0.0, value=0.0, step=0.01
        )
        np_venta = st.number_input(
            "Precio de Venta Base (€)", min_value=0.0, value=1.0, step=0.01
        )
        nstock = st.number_input("Existencias / Stock", value=0.0, step=1.0)
        ncad = st.date_input("Fecha de Caducidad", value=date.today())

        submitted = st.form_submit_button("Guardar en Inventario")
        if submitted and ncod and nart:
          nuevo = pd.DataFrame([{
              "codigo": ncod,
              "articulo": nart,
              "p_compra": np_compra,
              "p_venta": np_venta,
              "stock": nstock,
              "caducidad": str(ncad),
          }])
          st.session_state.inventario = pd.concat(
              [st.session_state.inventario, nuevo], ignore_index=True
          )
          st.success("🎉 ¡Artículo guardado con éxito!")
          st.rerun()

  # --- ALERTAS DE CADUCIDAD ---
  elif menu == "⚠️ Alertas de Caducidad":
    st.markdown("### ⚠️ Control de Alertas de Caducidad")
    st.markdown(
        "Aquí puedes revisar qué productos están próximos a caducar o ya han"
        " vencido."
    )

    hoy = date.today()
    inv = st.session_state.inventario.copy()

    # Convertir fecha a datetime para comparar
    inv["caducidad_dt"] = pd.to_datetime(inv["caducidad"]).dt.date

    caducados = inv[inv["caducidad_dt"] < hoy]
    por_caducar = inv[
        (inv["caducidad_dt"] >= hoy)
        & (inv["caducidad_dt"] <= pd.Timestamp(hoy.toordinal() + 30).date())
    ]

    st.markdown("#### 🔴 Productos Caducados")
    if not caducados.empty:
      st.error(
          "¡Atención! Hay productos que ya han superado su fecha de caducidad:"
      )
      st.dataframe(
          caducados[["codigo", "articulo", "stock", "caducidad"]],
          use_container_width=True,
      )
    else:
      st.success("✅ No hay ningún producto caducado.")

    Item_proximo = por_caducar
    st.markdown("#### 🟡 Productos Próximos a Caducar (Próximos 30 días)")
    if not Item_proximo.empty:
      st.warning("Revisa estos artículos, caducan pronto:")
      st.dataframe(
          Item_proximo[["codigo", "articulo", "stock", "caducidad"]],
          use_container_width=True,
      )
    else:
      st.success("✅ Todo en orden. No hay productos próximos a caducar.")

  # --- CONFIGURACIÓN DE NOMBRES ---
  elif menu == "⚙️ Configuración Nombres":
    if st.session_state.rol_activo != "Administrador":
      st.warning("⚠️ Solo el Administrador puede modificar los nombres.")
    else:
      st.markdown("### ⚙️ Personalizar Nombres de Turno y Administrador")
      with st.form("form_nombres"):
        nuevo_admin = st.text_input(
            "Nombre del Administrador", value=st.session_state.admin_nombre
        )
        nuevo_empleado = st.text_input(
            "Nombre del Empleado de Turno",
            value=st.session_state.empleado_nombre,
        )

        if st.form_submit_button("💾 Guardar Cambios"):
          st.session_state.admin_nombre = nuevo_admin
          st.session_state.empleado_nombre = nuevo_empleado
          st.success("🎉 ¡Nombres actualizados correctamente!")
          st.rerun()
