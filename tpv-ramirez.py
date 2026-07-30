import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="TPV Ramírez", page_icon="🛒", layout="wide")

# Inicialización del Session State
if "inventario" not in st.session_state:
    st.session_state.inventario = [
        {"codigo": "101", "desc": "Café con Leche", "costo": 0.80, "precio": 1.50, "iva": 10, "stock": 50.0, "caducidad": "31/12/2026"},
        {"codigo": "102", "desc": "Croissant de Mantequilla", "costo": 0.60, "precio": 1.20, "iva": 10, "stock": 30.0, "caducidad": "31/12/2026"},
        {"codigo": "103", "desc": "Agua Mineral 50cl", "costo": 0.30, "precio": 1.00, "iva": 21, "stock": 100.0, "caducidad": "31/12/2026"}
    ]

if "historial_ventas" not in st.session_state:
    st.session_state.historial_ventas = []

if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "rol_actual" not in st.session_state:
    st.session_state.rol_actual = "admin"

if "efectivo_caja" not in st.session_state:
    st.session_state.efectivo_caja = 150.0

# Barra lateral de navegación y control de roles
st.sidebar.title("🛒 TPV Ramírez")
st.sidebar.markdown("---")

rol = st.sidebar.selectbox("Rol de Usuario", ["admin", "empleado"], index=0 if st.session_state.rol_actual=="admin" else 1)
st.session_state.rol_actual = rol

selected_tab = st.sidebar.radio("Menú Principal", ["Caja / Ventas", "Historial", "Top / Menos Vendidos", "Inventario y Productos"])

st.sidebar.markdown("---")
st.sidebar.info(f"Caja actual: {st.session_state.efectivo_caja:.2f} €")

# --- MÓDULO 1: CAJA / VENTAS ---
if selected_tab == "Caja / Ventas":
    st.subheader("💳 Terminal de Venta")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        busqueda = st.text_input("Buscar producto por código o descripción")
        productos_filtrados = [p for p in st.session_state.inventario if busqueda.lower() in p["codigo"].lower() or busqueda.lower() in p["desc"].lower()] if busqueda else st.session_state.inventario
        
        for p in productos_filtrados:
            c_prod1, c_prod2, c_prod3 = st.columns([3, 2, 1])
            with c_prod1:
                st.write(f"**{p['desc']}** ({p['precio']:.2f} €)")
            with c_prod2:
                st.write(f"Stock: {p['stock']}")
            with c_prod3:
                if st.button("Añadir", key=f"add_{p['codigo']}"):
                    # Buscar si ya está en el carrito
                    en_carrito = next((item for item in st.session_state.carrito if item["codigo"] == p["codigo"]), None)
                    if en_carrito:
                        en_carrito["cant"] += 1.0
                    else:
                        st.session_state.carrito.append({
                            "codigo": p["codigo"],
                            "desc": p["desc"],
                            "precio": p["precio"],
                            "iva": p["iva"],
                            "cant": 1.0
                        })
                    st.rerun()

    with col2:
        st.markdown("### 🛍️ Carrito Actual")
        if not st.session_state.carrito:
            st.info("El carrito está vacío.")
        else:
            total_neto = 0
            for i, item in enumerate(st.session_state.carrito):
                subtotal = item["precio"] * item["cant"]
                total_neto += subtotal
                st.write(f"**{item['desc']}**")
                c_cant1, c_cant2 = st.columns(2)
                with c_cant1:
                    nueva_cant = st.number_input("Cant", value=float(item["cant"]), min_value=0.1, key=f"cant_{i}")
                    item["cant"] = nueva_cant
                with c_cant2:
                    st.write(f"{subtotal:.2f} €")
                if st.button("Eliminar", key=f"del_{i}"):
                    st.session_state.carrito.pop(i)
                    st.rerun()
                st.markdown("---")
            
            st.markdown(f"### Total: {total_neto:.2f} €")
            
            metodo_pago = st.selectbox("Método de Pago", ["Efectivo", "Tarjeta"])
            
            if st.button("Cobrar y Finalizar Venta", type="primary"):
                # Registrar venta
                nueva_venta = {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "items": list(st.session_state.carrito),
                    "total": total_neto,
                    "metodo": metodo_pago
                }
                st.session_state.historial_ventas.append(nueva_venta)
                
                # Descontar stock
                for item in st.session_state.carrito:
                    for p in st.session_state.inventario:
                        if p["codigo"] == item["codigo"]:
                            p["stock"] -= item["cant"]
                
                if metodo_pago == "Efectivo":
                    st.session_state.efectivo_caja += total_neto
                
                st.session_state.carrito = []
                st.success("¡Venta completada con éxito!")
                st.rerun()

# --- MÓDULO 2: HISTORIAL ---
elif selected_tab == "Historial":
    st.subheader("📋 Historial de Ventas")
    if st.session_state.historial_ventas:
        h_data = []
        for v in st.session_state.historial_ventas:
            h_data.append({
                "Fecha": v["fecha"],
                "Método": v["metodo"],
                "Total (€)": f"{v['total']:.2f}"
            })
        st.dataframe(pd.DataFrame(h_data), use_container_width=True, hide_index=True)
    else:
        st.info("No hay ventas registradas todavía.")

# --- MÓDULO 4: TOP / MENOS VENDIDOS ---
elif selected_tab == "Top / Menos Vendidos":
    st.subheader("🌱 Ranking de Productos")
    conteo = {p["codigo"]: {"desc": p["desc"], "cant": 0.0} for p in st.session_state.inventario}
    for v in st.session_state.historial_ventas:
        for item in v["items"]:
            if item["codigo"] in conteo:
                conteo[item["codigo"]]["cant"] += item["cant"]
                
    rank_df = pd.DataFrame(list(conteo.values())).sort_values(by="cant", ascending=False)
    st.dataframe(rank_df, use_container_width=True, hide_index=True)

# --- MÓDULO 5: INVENTARIO (SOLO ADMIN) ---
elif selected_tab == "Inventario y Productos":
    if st.session_state.rol_actual != "admin":
        st.error("⛔ ACCESO DENEGADO. Los empleados no pueden modificar el inventario.")
    else:
        st.subheader("📦 Gestión Exclusiva de Inventario (Admin)")
        st.dataframe(pd.DataFrame(st.session_state.inventario), use_container_width=True, hide_index=True)
        
        with st.form("nuevo_prod_admin"):
            st.write("Registrar o Modificar Artículo")
            ncod = st.text_input("Código de barras exacto")
            ndesc = st.text_input("Descripción del producto")
            ncosto = st.number_input("Costo (€)", value=1.0)
            nprec = st.number_input("Precio de Venta (€)", value=2.0)
            niva = st.selectbox("IVA %", [21, 10, 4])
            nstock = st.number_input("Stock actual", value=10.0)
            ncad = st.text_input("Caducidad (DD/MM/AAAA)", value="31/12/2026")
            
            if st.form_submit_button("Guardar Cambios de Inventario"):
                existente = next((p for p in st.session_state.inventario if p["codigo"] == ncod), None)
                if existente:
                    existente["desc"] = ndesc
                    existente["costo"] = ncosto
                    existente["precio"] = nprec
                    existente["iva"] = niva
                    existente["stock"] = nstock
                    existente["caducidad"] = ncad
                    st.success("¡Artículo actualizado correctamente!")
                else:
                    st.session_state.inventario.append({
                        "codigo": ncod,
                        "desc": ndesc,
                        "costo": ncosto,
                        "precio": nprec,
                        "iva": niva,
                        "stock": nstock,
                        "caducidad": ncad
                    })
                    st.success("¡Nuevo artículo registrado con éxito!")
                st.rerun()
