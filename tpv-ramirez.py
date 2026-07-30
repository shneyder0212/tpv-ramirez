import sqlite3
from flask import Flask, request, jsonify, g
from datetime import datetime

app = Flask(__name__)
DATABASE = 'tienda.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        
        # 1. Tabla de usuarios
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('admin', 'empleado'))
            )
        ''')
        
        # 2. Tabla de productos con soporte para IVA (21, 10, 4)
        db.execute('''
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
        
        # 3. Carga inicial del inventario
        cursor = db.execute('SELECT COUNT(*) FROM productos')
        count = cursor.fetchone()[0]
        
        if count == 0:
            productos_iniciales = [
                ('000000000001', 'SAZON LIQUIDO RANCHERO 400ML', 0.00, 0.00, 2.47, 21),
                ('000000000002', 'GANDULES VERDES CON COCO GOYA', 6.00, 2.11, 2.72, 4),
                ('000000000003', 'OREGANO RANCHERO EN POLVO 90GR', 12.00, 0.00, 2.47, 10),
                ('000000000004', 'FRIJOLES NEGROS PLEBEYO 400GR', 0.00, 0.00, 2.06, 4),
                ('000000000020', 'COCA COLA LATA 330 ML', 61.00, 0.61, 1.23, 21),
                ('8410199026418', 'CERVEZA POKER 330ML', 0.00, 0.00, 2.06, 21),
            ]
            db.executemany('''
                INSERT INTO productos (codigo, nombre, existencias, costo_un, precio_base, iva)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', productos_iniciales)
            db.commit()

def obtener_usuario_actual():
    rol = request.headers.get('X-User-Rol', 'empleado')
    return {'rol': rol}

# Listar productos con paginación, búsqueda por texto o lector de códigos de barras
@app.route('/api/productos', methods=['GET'])
def listar_productos():
    usuario = obtener_usuario_actual()
    db = get_db()
    
    busqueda = request.args.get('q', '').strip()
    codigo_exacto = request.args.get('codigo', '').strip()
    limite = int(request.args.get('limit', 15))
    pagina = int(request.args.get('page', 1))
    offset = (pagina - 1) * limite

    query = 'SELECT * FROM productos WHERE 1=1'
    params = []

    if codigo_exacto:
        query += ' AND codigo = ?'
        params.append(codigo_exacto)
    elif busqueda:
        query += ' AND (nombre LIKE ? OR codigo LIKE ?)'
        params.extend([f'%{busqueda}%', f'%{busqueda}%'])
    else:
        query += ' LIMIT ? OFFSET ?'
        params.extend([limite, offset])

    cursor = db.execute(query, params)
    productos = cursor.fetchall()
    
    resultado = []
    for p in productos:
        precio_con_iva = round(p['precio_base'] * (1 + (p['iva'] / 100.0)), 2)
        prod_dict = {
            'id': p['id'],
            'codigo': p['codigo'],
            'nombre': p['nombre'],
            'existencias': p['existencias'],
            'precio_base': p['precio_base'],
            'iva_porcentaje': p['iva'],
            'precio_venta_con_iva': precio_con_iva
        }
        if usuario['rol'] == 'admin':
            prod_dict['costo_un'] = p['costo_un']
        resultado.append(prod_dict)
        
    return jsonify({
        'total_encontrados': len(resultado),
        'pagina_actual': pagina,
        'productos': resultado
    }), 200

# Endpoint para generar el ticket de venta idéntico al modelo de la foto
@app.route('/api/tickets', methods=['POST'])
def generar_ticket():
    data = request.get_json()
    items = data.get('items', []) # Lista de elementos: [{'codigo': '...', 'cantidad': X}]
    entregado = float(data.get('entregado', 0.0))
    cajero = data.get('cajero', 'RAFELIN MENDEZ')
    
    db = get_db()
    
    ticket_items = []
    desglose_iva = {21.0: {'base': 0.0, 'cuota': 0.0}, 10.0: {'base': 0.0, 'cuota': 0.0}, 4.0: {'base': 0.0, 'cuota': 0.0}}
    
    for item in items:
        codigo = item.get('codigo')
        cantidad = float(item.get('cantidad', 1))
        
        cursor = db.execute('SELECT * FROM productos WHERE codigo = ?', (codigo,))
        prod = cursor.fetchone()
        
        if prod:
            precio_base = prod['precio_base']
            iva_porc = float(prod['iva'])
            importe_base = round(precio_base * cantidad, 2)
            
            if iva_porc not in desglose_iva:
                desglose_iva[iva_porc] = {'base': 0.0, 'cuota': 0.0}
                
            desglose_iva[iva_porc]['base'] += importe_base
            cuota_iva_item = importe_base * (iva_porc / 100.0)
            desglose_iva[iva_porc]['cuota'] += cuota_iva_item
            
            ticket_items.append({
                'uds': cantidad,
                'articulo': prod['nombre'],
                'precio': precio_base,
                'importe': importe_base
            })
            
    total_con_iva = sum([vals['base'] + vals['cuota'] for vals in desglose_iva.values()])
    cambio = round(entregado - total_con_iva, 2) if entregado >= total_con_iva else 0.0
    
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M")
    
    # Construcción exacta del formato de ticket físico
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
    for ti in ticket_items:
        ticket_texto += f"{ti['uds']:<3} {ti['articulo'][:22]:<22} {ti['precio']:>5.2f}€ {ti['importe']:>6.2f}€\n"
        
    ticket_texto += f"""----------------------------------------
                  TOTAL        {total_con_iva:.2f} €
----------------------------------------
   BASE IMPONIBLE    %IVA        IVA
"""
    for porc, vals in desglose_iva.items():
        if vals['base'] > 0:
            ticket_texto += f"       {vals['base']:>8.2f} €    {porc:>4.1f}     {vals['cuota']:>6.2f} €\n"
            
    ticket_texto += f"""----------------------------------------
ENTREGADO                {entregado:.2f} € CAMBIO      {cambio:.2f} €
EFECTIVO
----------------------------------------
LE ATENDIÓ {cajero}

GRACIAS POR SU COMPRA. ES IMPRESCINDIBLE LA
PRESENTACION DEL TICKET PARA CUALQUIER DEVOLUCION
"""
    
    return jsonify({
        'ticket_formateado': ticket_texto,
        'total_general': total_con_iva,
        'cambio': cambio
    }), 200

# Endpoint de actualización para el administrador
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    usuario = obtener_usuario_actual()
    if usuario['rol'] != 'admin':
        return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
        
    data = request.get_json()
    db = get_db()
    db.execute('''
        UPDATE productos 
        SET costo_un = COALESCE(?, costo_un),
            precio_base = COALESCE(?, precio_base),
            iva = COALESCE(?, iva),
            existencias = COALESCE(?, existencias)
        WHERE id = ?
    ''', (data.get('costo_un'), data.get('precio_base'), data.get('iva'), data.get('existencias'), id))
    db.commit()
    
    return jsonify({'mensaje': 'Actualizado correctamente'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
