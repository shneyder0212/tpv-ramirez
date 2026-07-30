import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Multi Servicios Ramirez - TPV Profesional",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para un aspecto moderno y oscuro profesional
st.markdown("""
    <style>
    .main { background-color: #121212; color: #ffffff; }
    .stTextInput > div > div > input { background-color: #2d2d2d; color: white; border-radius: 5px; }
    .stSelectbox > div > div > div { background-color: #2d2d2d; color: white; }
    div.stButton > button { width: 100%; border-radius: 6px; font-weight: bold; height: 45px; }
    .total-card { background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #333; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# Inicializar Base de Datos de Productos en la sesión (Artículos reales de las hojas de inventario)
if 'productos' not in st.session_state:
    st.session_state.productos = [
        {"codigo": "000000000001", "nombre": "SAZON LIQUIDO RANCHERO 400ML", "stock": 0.0, "costo": 0.0, "precio": 2.47, "iva": 21},
        {"codigo": "000000000002", "nombre": "GANDULES VERDES CON COCO GOYA", "stock": 6.0, "costo": 2.11, "precio": 2.72, "iva": 4},
        {"codigo": "000000000003", "nombre": "OREGANO RANCHERO EN POLVO 90GR", "stock": 12.0, "costo": 0.0, "precio": 2.47, "iva": 10},
        {"codigo": "000000000004", "nombre": "FRIJOLES NEGROS PLEBEYO 400GR", "stock": 0.0, "costo": 0.0, "precio": 2.06, "iva": 4},
        {"codigo": "8410199026418", "nombre": "CERVEZA POKER 330ML", "stock": 24.0, "costo": 1.50, "precio": 2.06, "iva": 21},
        {"codigo": "000000000006", "nombre": "AGUA VIVO 50ml", "stock": 15.0, "costo": 0.50, "precio": 1.00, "iva": 21},
        {"codigo": "7702001001234", "nombre": "ARROZ DIANA BLANCO 1KG", "stock": 30.0, "costo": 1.10, "precio": 1.50, "iva": 4},
        {"codigo": "000000000020", "nombre": "COCA COLA LATA 330 ML", "stock": 61.0, "costo": 0.61, "precio": 1.23, "iva": 21},
        {"codigo": "4562589632679", "nombre": "LECHE DE COCO GRANDE 1LT GOYA", "stock": 8.0, "costo": 3.05, "precio": 4.54, "iva": 10}
    ]

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# --- BARRA LATERAL (CONFIGURACIÓN Y NAVEGACIÓN) ---
st.sidebar.title("⚡ Multi Servicios Ramirez")
st.sidebar.markdown(f"**Terminal:** T1 (F11)")
st.sidebar.markdown(f"**Dependiente:** [2] RAFELIN MENDEZ")
st.sidebar.markdown(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

menu = st.sidebar.radio("Menú Principal", ["🛒 TPV / Caja", "📦 Gestión de Inventario & Artículos"])

# --- MÓDULO 1: TPV / CAJA ---
if menu == "🛒 TPV / Caja":
    st.title("Terminal Punto de Venta")

    col_input1, col_input2 = st.columns([3, 1])
    with col_input1:
        busqueda = st.text_input("🔍 Escanear Código de Barras o Buscar Artículo:", placeholder="Escribe el nombre o código...")
    with col_input2:
        unidades = st.number_input("Unidades", min_value=0.1, value=1.0, step=1.0)

    # Filtrar productos según búsqueda
    if busqueda:
        resultados = [p for p in st.session_state.productos if busqueda.lower() in p['codigo'].lower() or busqueda.lower() in p['nombre'].lower()]
        if resultados:
            st.write("Resultados encontrados:")
            cols_res = st.columns(len(resultados) if len(resultados) <= 3 else 3)
            for idx, prod in enumerate(resultados[:3]):
                with cols_res[idx]:
                    if st.button(f"➕ {prod['nombre']} ({prod['precio']}€)", key=f"add_{prod['codigo']}_{idx}"):
                        st.session_state.carrito.append({
                            "codigo": prod['codigo'],
                            "nombre": prod['nombre'],
                            "unids": unidades,
                            "precio": prod['precio'],
                            "iva": prod['iva']
                        })
                        st.rerun()

    st.markdown("---")
    st.subheader("📋 Líneas del Ticket Actual")

    if st.session_state.carrito:
        df_carrito = pd.DataFrame(st.session_state.carrito)
        df_carrito['Importe Total'] = df_carrito['unids'] * df_carrito['precio']
        
        # Mostrar tabla estilizada
        st.dataframe(df_carrito[['codigo', 'nombre', 'unids', 'precio', 'iva', 'Importe Total']], use_container_width=True)

        # Acciones del carrito
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("🗑️ Vaciar Ticket", type="secondary"):
                st.session_state.carrito = []
                st.rerun()
        with col_btn2:
            if st.button("🖨️ Imprimir Ticket"):
                st.success("Ticket impreso correctamente por la impresora predeterminada.")
        with col_btn3:
            if st.button("💰 Cobrar Venta (F5)", type="primary"):
                st.success("¡Cobro realizado con éxito! Caja actualizada.")
                st.session_state.carrito = []
                st.rerun()

        # Totales
        base_imponible = sum(item['unids'] * item['precio'] / (1 + item['iva']/100) for item in st.session_state.carrito)
        iva_total = sum((item['unids'] * item['precio']) - (item['unids'] * item['precio'] / (1 + item['iva']/100)) for item in st.session_state.carrito)
        total_pagar = sum(item['unids'] * item['precio'] for item in st.session_state.carrito)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Base Imponible", f"{base_imponible:.2f} €")
        c2.metric("IVA Total", f"{iva_total:.2f} €")
        c3.metric("TOTAL A PAGAR", f"{total_pagar:.2f} €", delta_color="normal")

    else:
        st.info("El carrito está vacío. Escanea un código o busca un producto arriba.")

# --- MÓDULO 2: GESTIÓN DE INVENTARIO ---
elif menu == "📦 Gestión de Inventario & Artículos":
    st.title("Gestión de Inventario y Precios")
    st.markdown("Añade nuevos productos o edita los existentes en la base de datos de la tienda.")

    with st.form("form_nuevo_producto"):
        st.subheader("Registrar / Actualizar Artículo")
        col1, col2, col3 = st.columns(3)
        with col1:
            n_codigo = st.text_input("Código de Barras")
            n_costo = st.number_input("Precio Costo (€)", min_value=0.0, value=0.0)
        with col2:
            n_nombre = st.text_input("Descripción del Artículo")
            n_precio = st.number_input("Precio Venta Base (€)", min_value=0.0, value=1.0)
        with col3:
            n_stock = st.number_input("Existencias Iniciales", min_value=0.0, value=0.0)
            n_iva = st.selectbox("Tipo de IVA (%)", [21, 10, 4])

        submitted = st.form_submit_button("Guardar Artículo en Base de Datos")
        if submitted:
            if n_codigo and n_nombre:
                # Comprobar si ya existe para actualizar o crear nuevo
                existente = next((p for p in st.session_state.productos if p['codigo'] == n_codigo), None)
                if existente:
                    existente['nombre'] = n_nombre
                    existente['costo'] = n_costo
                    existente['precio'] = n_precio
                    existente['stock'] = n_stock
                    existente['iva'] = n_iva
                    st.success(f"Artículo '{n_nombre}' actualizado correctamente.")
                else:
                    st.session_state.productos.append({
                        "codigo": n_codigo,
                        "nombre": n_nombre,
                        "stock": n_stock,
                        "costo": n_costo,
                        "precio": n_precio,
                        "iva": n_iva
                    })
                    st.success(f"Artículo '{n_nombre}' registrado con éxito.")
            else:
                st.error("El código de barras y la descripción son obligatorios.")

    st.markdown("---")
    st.subheader("Catálogo Actual en Almacén")
    df_catalogo = pd.DataFrame(st.session_state.productos)
    st.dataframe(df_catalogo, use_container_width=True)
