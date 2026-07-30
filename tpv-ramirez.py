import sqlite3
from flask import Flask, request, jsonify, g

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
        # Tabla de usuarios con roles ('admin' o 'empleado')
        db.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('admin', 'empleado'))
            )
        ''')
        # Tabla de productos con precio de compra y precio de venta
        db.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        ''')
        db.commit()

# Identificador de rol basado en cabecera HTTP (puedes adaptarlo a tu sistema de login/JWT)
def obtener_usuario_actual():
    rol = request.headers.get('X-User-Rol', 'empleado')
    return {'rol': rol}

@app.route('/api/productos', methods=['GET'])
def listar_productos():
    usuario = obtener_usuario_actual()
    db = get_db()
    cursor = db.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    
    resultado = []
    for p in productos:
        prod_dict = {
            'id': p['id'],
            'nombre': p['nombre'],
            'precio_venta': p['precio_venta'],
            'stock': p['stock']
        }
        # RESTRICCIÓN: Solo el administrador puede visualizar el precio de compra
        if usuario['rol'] == 'admin':
            prod_dict['precio_compra'] = p['precio_compra']
            
        resultado.append(prod_dict)
        
    return jsonify(resultado), 200

@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    usuario = obtener_usuario_actual()
    
    # RESTRICCIÓN: Solo el administrador puede actualizar precios de compra y venta
    if usuario['rol'] != 'admin':
        return jsonify({'error': 'Acceso denegado. No tienes permisos para modificar precios.'}), 403
        
    data = request.get_json()
    nombre = data.get('nombre')
    precio_compra = data.get('precio_compra')
    precio_venta = data.get('precio_venta')
    stock = data.get('stock')
    
    db = get_db()
    db.execute('''
        UPDATE productos 
        SET nombre = COALESCE(?, nombre),
            precio_compra = COALESCE(?, precio_compra),
            precio_venta = COALESCE(?, precio_venta),
            stock = COALESCE(?, stock)
        WHERE id = ?
    ''', (nombre, precio_compra, precio_venta, stock, id))
    db.commit()
    
    return jsonify({'mensaje': 'Precios y datos actualizados correctamente'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
