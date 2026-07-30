import sqlite3
import streamlit as datetime_mod
from datetime import datetime
import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Multi Servicios Ramirez - TPV", layout="wide")

DATABASE = 'tienda.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            existencias REAL DEFAULT 0,
            costo_un REAL DEFAULT 0,
            precio_base REAL NOT NULL,
            iva INTEGER DEFAULT 21 CHECK(iva IN (21, 10, 4))
        )
    ''')
    
    # Carga inicial si está vacío
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_iniciales = [
            ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 0.00, 0.00, 2.47, 21),
            ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.00, 2.11, 2.72, 4),
            ('000000000003', 'OREGANO RANCHERO EN POLVO 90GR', 12.00, 0.00, 2.47, 10),
            ('000000000004', 'FRIJOLES NEGROS PLEBEYO 400GR', 0.00, 0.00, 2.06, 4),
            ('000000000020', 'COCA COLA LATA 330 ML', 61.00, 0.61, 1.23, 21),
            ('8410199026418', 'CERVEZA POKER 330ML', 10.00, 1.50, 2.06, 21),
        ]
        cursor.executemany('''
            INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', productos_iniciales)
        conn.commit()
    conn.close()

init_db()

# Interfaz principal
st.title("🛒 Multi Servicios Ramirez - TPV")

# Selector de Rol en la barra lateral
rol = st.sidebar.selectbox("Rol de Usuario", ["Empleado", "Administrador"])
cajero_nombre = st.sidebar.text_input("Nombre del Cajero", "RAFELIN MENDEZ")

conn = get_connection()

# Sección de Búsqueda y Lector de Códigos
st.subheader("🔍 Búsqueda de Productos / Lector de Barras")
busqueda_input = st.text_input("Escanee el código de barras o escriba el nombre del artículo:", "")

query = "SELECT * FROM productos WHERE 1=1"
params = []

if busqueda_input:
    query += " AND (codigo = ? OR nombre LIKE ?)"
    params = [busqueda_input, f"%{busqueda_input}%"]
else:
    # Paginación visual: muestra solo 10 por defecto en pantalla para mantener la app ligera
    query += " LIMIT 10"

cursor = conn.cursor()
cursor.execute(query, params)
productos_visibles = cursor.fetchall()

st.write(f"Mostrando {len(productos_visibles)} productos en vista rápida (el inventario completo está guardado en el sistema):")

# Tabla interactiva o listado
for p in productos_visibles:
    precio_con_iva = round(p['precio_base'] * (1 + (p['iva'] / 100.0)), 2)
    cols = st.columns([2, 4, 1, 1, 1])
    cols[0].text(p['codigo'])
    cols[1].text(p['nombre'])
    cols[2].text(f"{precio_con_iva:.2f} €")
    cols[3].text(f"Stock: {p['existencias']}")
    
    if rol == "Administrador":
        nuevo_precio = cols[4].number_input("Precio Base", value=p['precio_base'], key=f"p_{p['id']}")
        if nuevo_precio != p['precio_base']:
            cursor.execute("UPDATE productos SET precio_base = ? WHERE id = ?", (nuevo_precio, p['id']))
            conn.commit()

# Carrito de Venta simulado
st.markdown("---")
st.subheader("🛍️ Registrar Venta y Generar Ticket")

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

codigo_agregar = st.text_input("Añadir al carrito por código exacto o pistola:")
cantidad_agregar = st.number_input("Cantidad", min_value=1.0, value=1.0, step=1.0)

if st.button("Añadir Artículo"):
    cursor.execute("SELECT * FROM productos WHERE codigo = ?", (codigo_agregar,))
    prod_encontrado = cursor.fetchone()
    if prod_encontrado:
        st.session_state.carrito.append({
            'codigo': prod_encontrado['codigo'],
            'nombre': prod_encontrado['nombre'],
            'precio_base': prod_encontrado['precio_base'],
            'iva': float(prod_encontrado['iva']),
            'cantidad': cantidad_agregar
        })
        st.success(f"Añadido: {prod_encontrado['nombre']}")
    else:
        st.error("Producto no encontrado con ese código.")

if st.session_state.carrito:
    st.write("### Artículos en el Ticket Actual:")
    total_general = 0.0
    desglose_iva = {21.0: {'base': 0.0, 'cuota': 0.0}, 10.0: {'base': 0.0, 'cuota': 0.0}, 4.0: {'base': 0.0, 'cuota': 0.0}}
    
    for idx, item in enumerate(st.session_state.carrito):
        importe_base = round(item['precio_base'] * item['cantidad'], 2)
        total_general += importe_base * (1 + item['iva'] / 100.0)
        desglose_iva[item['iva']]['base'] += importe_base
        desglose_iva[item['iva']]['cuota'] += importe_base * (item['iva'] / 100.0)
        st.text(f"- {item['cantidad']}x {item['nombre']} ({item['precio_base']}€ base) = {importe_base}€")

    efectivo_entregado = st.number_input("Efectivo Entregado (€)", min_value=0.0, value=float(total_general))
    
    if st.button("🖨️ Imprimir Ticket de Venta"):
        cambio = round(efectivo_entregado - total_general, 2) if efectivo_entregado >= total_general else 0.0
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M")
        
        # Estructura idéntica al ticket físico de tu foto
        ticket_texto = f"""
       MULTI SERVICIOS RAMIREZ
          AVDA DR FLEMING 9
          24009 LEON ESPANA

Telf. 655766134    NIF  02799425 A

Ticket N° 01T12600002978          {fecha_actual}
                                    {hora_actual}
----------------------------------------
UDS. ARTICULO             PRECIO  IMPORTE
----------------------------------------
"""
        for ti in st.session_state.carrito:
            imp = round(ti['precio_base'] * ti['cantidad'], 2)
            ticket_texto += f"{ti['cantidad']:<3} {ti['nombre'][:22]:<22} {ti['precio_base']:>5.2f}€ {imp:>6.2f}€\n"
            
        ticket_texto += f"""----------------------------------------
                  TOTAL        {total_general:.2f} €
----------------------------------------
   BASE IMPONIBLE    %IVA        IVA
"""
        for porc, vals in desglose_iva.items():
            if vals['base'] > 0:
                ticket_texto += f"       {vals['base']:>8.2f} €    {porc:>4.1f}     {vals['cuota']:>6.2f} €\n"
                
        ticket_texto += f"""----------------------------------------
ENTREGADO                {efectivo_entregado:.2f} € CAMBIO      {cambio:.2f} €
EFECTIVO
----------------------------------------
LE ATENDIÓ {cajero_nombre}

GRACIAS POR SU COMPRA. ES IMPRESCINDIBLE LA
PRESENTACION DEL TICKET PARA CUALQUIER DEVOLUCION
"""
        st.text_area("Ticket Generado para Impresora Térmica:", ticket_texto, height=300)
        st.success(f"Cambio a devolver al cliente: **{cambio:.2f} €**")
        
        if st.button("Limpiar Carrito / Siguiente Venta"):
            st.session_state.carrito = []
            st.rerun()

conn.close()
