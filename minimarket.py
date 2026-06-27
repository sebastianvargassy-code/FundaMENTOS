from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import datetime
import functools  # <-- CORRECCIÓN 1: importar functools

# ---------- CREAR LA APLICACIÓN ----------
app = Flask(__name__)
app.secret_key = 'clave_secreta_2026'  # Cambiar en producción

# ---------- USUARIO ADMIN (hardcodeado) ----------
ADMIN_USER = {
    'username': 'admin',
    'password': 'admin123'   # ¡Cambiar en producción!
}

# ---------- PRODUCTOS (en memoria) ----------
PRODUCTOS = [
    {"id": 1, "nombre": "Galleta soda", "peso": "6 unidades (222 gr)", "precio": 3.30, "img": "i1.jpg"},
    {"id": 2, "nombre": "Coca Cola", "peso": "500 ml", "precio": 3.50, "img": "i2.jpg"},
    {"id": 3, "nombre": "Leche Gloria", "peso": "390 gr", "precio": 4.20, "img": "i3.jpg"},
    {"id": 4, "nombre": "Yogurt Laive", "peso": "1000 gr", "precio": 6.50, "img": "i4.jpg"},
    {"id": 5, "nombre": "Pan en bolsa", "peso": "500 gr", "precio": 8.50, "img": "i5.jpg"},
    {"id": 6, "nombre": "Galletas de vainilla", "peso": "6 unidades (222 gr)", "precio": 4.70, "img": "i6.jpg"},
    {"id": 7, "nombre": "Atún en lata", "peso": "140 gr", "precio": 5.80, "img": "i7.jpg"},
    {"id": 8, "nombre": "Café Kirma", "peso": "180 gr", "precio": 21.90, "img": "i8.jpg"},
    {"id": 9, "nombre": "Huevos", "peso": "15 unidades", "precio": 9.50, "img": "i9.jpg"},
    {"id": 10, "nombre": "Chocolate Triangulo", "peso": "30 gr", "precio": 2.50, "img": "i10.jpg"},
    {"id": 11, "nombre": "Gaseosa KR", "peso": "1500 ml", "precio": 3.50, "img": "i11.jpg"},
    {"id": 12, "nombre": "Gaseosa sprite", "peso": "1500 ml", "precio": 6.50, "img": "i12.jpg"},
    {"id": 13, "nombre": "Galletas oreo", "peso": "432 gr", "precio": 8.20, "img": "i13.jpg"},
    {"id": 14, "nombre": "Mayonesa", "peso": "190 gr", "precio": 5.80, "img": "i14.jpg"},
    {"id": 15, "nombre": "Mermelada", "peso": "320 gr", "precio": 5.50, "img": "i15.jpg"},
    {"id": 16, "nombre": "Jamón San Fernando", "peso": "200 gr", "precio": 9.50, "img": "i16.jpg"},
    {"id": 17, "nombre": "Margarina Manti", "peso": "225 gr", "precio": 3.50, "img": "i17.jpg"},
    {"id": 18, "nombre": "Mantequilla Laive", "peso": "200 gr", "precio": 7.50, "img": "i18.jpg"},
    {"id": 19, "nombre": "Café Ecco", "peso": "80 gr", "precio": 8.50, "img": "i19.jpg"},
    {"id": 20, "nombre": "Café Altomayo", "peso": "170 gr", "precio": 25.10, "img": "i20.jpg"},
]

# ---------- CLIENTES (en memoria) ----------
CLIENTES = [
    {"id": 1,  "nombre": "Ana Gómez",           "email": "ana.gomez@gmail.com",          "telefono": "987654321", "fecha_registro": "14/06"},
    {"id": 2,  "nombre": "Carlos Ruíz",          "email": "carlos.ruiz@gmail.com",        "telefono": "912345678", "fecha_registro": "16/06"},
    {"id": 3,  "nombre": "María López",          "email": "maria.lopez@hotmail.com",      "telefono": "934567890", "fecha_registro": "01/06"},
    {"id": 4,  "nombre": "José Martínez",        "email": "jose.martinez@gmail.com",      "telefono": "956789012", "fecha_registro": "02/06"},
    {"id": 5,  "nombre": "Lucía Fernández",      "email": "lucia.fer@gmail.com",          "telefono": "978901234", "fecha_registro": "02/06"},
    {"id": 6,  "nombre": "Pedro Sánchez",        "email": "pedro.san@gmail.com",          "telefono": "901234567", "fecha_registro": "03/06"},
    {"id": 7,  "nombre": "Sofía García",         "email": "sofia.garcia@hotmail.com",     "telefono": "923456789", "fecha_registro": "03/06"},
    {"id": 8,  "nombre": "Diego Rodríguez",      "email": "diego.rod@gmail.com",          "telefono": "945678901", "fecha_registro": "04/06"},
    {"id": 9,  "nombre": "Valentina Torres",     "email": "valen.torres@gmail.com",       "telefono": "967890123", "fecha_registro": "04/06"},
    {"id": 10, "nombre": "Andrés Ramírez",       "email": "andres.ram@gmail.com",         "telefono": "989012345", "fecha_registro": "05/06"},
    {"id": 11, "nombre": "Camila Flores",        "email": "camila.flores@gmail.com",      "telefono": "910234567", "fecha_registro": "05/06"},
    {"id": 12, "nombre": "Mateo Díaz",           "email": "mateo.diaz@hotmail.com",       "telefono": "932456789", "fecha_registro": "06/06"},
    {"id": 13, "nombre": "Isabella Morales",     "email": "isabella.mor@gmail.com",       "telefono": "954678901", "fecha_registro": "06/06"},
    {"id": 14, "nombre": "Sebastián Herrera",    "email": "sebas.her@gmail.com",          "telefono": "976890123", "fecha_registro": "07/06"},
    {"id": 15, "nombre": "Mariana Vargas",       "email": "mariana.var@gmail.com",        "telefono": "998012345", "fecha_registro": "07/06"},
    {"id": 16, "nombre": "Nicolás Castillo",     "email": "nico.cas@gmail.com",           "telefono": "920134567", "fecha_registro": "08/06"},
    {"id": 17, "nombre": "Gabriela Reyes",       "email": "gaby.reyes@hotmail.com",       "telefono": "942356789", "fecha_registro": "08/06"},
    {"id": 18, "nombre": "Daniel Mendoza",       "email": "daniel.men@gmail.com",         "telefono": "964578901", "fecha_registro": "09/06"},
    {"id": 19, "nombre": "Paula Guerrero",       "email": "paula.gue@gmail.com",          "telefono": "986790123", "fecha_registro": "09/06"},
    {"id": 20, "nombre": "Alejandro Cruz",       "email": "ale.cruz@gmail.com",           "telefono": "908912345", "fecha_registro": "10/06"},
    {"id": 21, "nombre": "Fernanda Ortiz",       "email": "fer.ortiz@gmail.com",          "telefono": "931034567", "fecha_registro": "10/06"},
    {"id": 22, "nombre": "Julián Silva",         "email": "julian.silva@hotmail.com",     "telefono": "953256789", "fecha_registro": "10/06"},
    {"id": 23, "nombre": "Daniela Romero",       "email": "dani.romero@gmail.com",        "telefono": "975478901", "fecha_registro": "11/06"},
    {"id": 24, "nombre": "Emilio Navarro",       "email": "emilio.nav@gmail.com",         "telefono": "997690123", "fecha_registro": "11/06"},
    {"id": 25, "nombre": "Renata Peña",          "email": "renata.pen@gmail.com",         "telefono": "919812345", "fecha_registro": "12/06"},
    {"id": 26, "nombre": "Tomás Aguilar",        "email": "tomas.agu@gmail.com",          "telefono": "941034567", "fecha_registro": "12/06"},
    {"id": 27, "nombre": "Natalia Ríos",         "email": "natalia.rios@hotmail.com",     "telefono": "963256789", "fecha_registro": "13/06"},
    {"id": 28, "nombre": "Samuel Cortés",        "email": "samuel.cor@gmail.com",         "telefono": "985478901", "fecha_registro": "13/06"},
    {"id": 29, "nombre": "Andrea Salazar",       "email": "andrea.sal@gmail.com",         "telefono": "907690123", "fecha_registro": "13/06"},
    {"id": 30, "nombre": "Felipe Medina",        "email": "felipe.med@gmail.com",         "telefono": "929812345", "fecha_registro": "14/06"},
    {"id": 31, "nombre": "Laura Domínguez",      "email": "laura.dom@gmail.com",          "telefono": "952034567", "fecha_registro": "14/06"},
    {"id": 32, "nombre": "Cristóbal Vega",       "email": "cristobal.veg@hotmail.com",    "telefono": "974256789", "fecha_registro": "15/06"},
    {"id": 33, "nombre": "Javiera Soto",         "email": "javiera.soto@gmail.com",       "telefono": "996478901", "fecha_registro": "15/06"},
    {"id": 34, "nombre": "Benjamín León",        "email": "benja.leon@gmail.com",         "telefono": "918690123", "fecha_registro": "15/06"},
    {"id": 35, "nombre": "Constanza Paredes",    "email": "constanza.par@gmail.com",      "telefono": "940812345", "fecha_registro": "16/06"},
    {"id": 36, "nombre": "Ricardo Campos",       "email": "ricardo.cam@gmail.com",        "telefono": "962034567", "fecha_registro": "16/06"},
    {"id": 37, "nombre": "Alejandra Miranda",    "email": "alejandra.mir@hotmail.com",    "telefono": "984256789", "fecha_registro": "17/06"},
    {"id": 38, "nombre": "Mauricio Solano",      "email": "mauricio.sol@gmail.com",       "telefono": "906478901", "fecha_registro": "17/06"},
    {"id": 39, "nombre": "Carolina Aguayo",      "email": "caro.aguayo@gmail.com",        "telefono": "928690123", "fecha_registro": "18/06"},
    {"id": 40, "nombre": "Esteban Delgado",      "email": "esteban.del@gmail.com",        "telefono": "950812345", "fecha_registro": "18/06"},
    {"id": 41, "nombre": "Valeria Cordero",      "email": "valeria.cor@gmail.com",        "telefono": "972034567", "fecha_registro": "19/06"},
    {"id": 42, "nombre": "Ignacio Bravo",        "email": "ignacio.brav@hotmail.com",     "telefono": "994256789", "fecha_registro": "19/06"},
    {"id": 43, "nombre": "Antonia Figueroa",     "email": "antonia.fig@gmail.com",        "telefono": "916478901", "fecha_registro": "20/06"},
    {"id": 44, "nombre": "Matías Espinoza",      "email": "matias.esp@gmail.com",         "telefono": "938690123", "fecha_registro": "20/06"},
    {"id": 45, "nombre": "Florencia Tapia",      "email": "florencia.tap@gmail.com",      "telefono": "960812345", "fecha_registro": "21/06"},
    {"id": 46, "nombre": "Joaquín Arrieta",      "email": "joaquin.arr@gmail.com",        "telefono": "982034567", "fecha_registro": "22/06"},
    {"id": 47, "nombre": "Javiera Cáceres",      "email": "javiera.cac@hotmail.com",      "telefono": "904256789", "fecha_registro": "23/06"},
    {"id": 48, "nombre": "Agustín Rojas",        "email": "agustin.roj@gmail.com",        "telefono": "926478901", "fecha_registro": "24/06"},
    {"id": 49, "nombre": "Emilia Fuentes",       "email": "emilia.fue@gmail.com",         "telefono": "948690123", "fecha_registro": "25/06"},
    {"id": 50, "nombre": "Vicente Barrera",      "email": "vicente.bar@gmail.com",        "telefono": "970812345", "fecha_registro": "26/06"},
]
next_cliente_id = 3

# ---------- VENTAS REGISTRADAS ----------
VENTAS = [
    {
        "id": 1,
        "fecha": "18/06",
        "productos": [{"nombre": "Coca Cola", "cantidad": 2, "precio": 3.50}],
        "metodo_pago": "Efectivo",
        "total": 7.00
    }
]
next_venta_id = 2

# ---------- DECORADOR PARA PROTEGER RUTAS ADMIN ----------
def login_required(f):
    @functools.wraps(f)  # <-- CORRECCIÓN 2: preservar el __name__ de cada función
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# ---------- RUTAS DE PÁGINAS PÚBLICAS ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html', productos=PRODUCTOS)

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER['username'] and password == ADMIN_USER['password']:
            session['admin_logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

# ---------- DASHBOARD ADMIN ----------
@app.route('/admin')
@login_required
def dashboard():
    total_productos = len(PRODUCTOS)
    precio_promedio = sum(p['precio'] for p in PRODUCTOS) / total_productos if total_productos > 0 else 0
    total_clientes = len(CLIENTES)

    ventas_mes = sum(v['total'] for v in VENTAS)
    variacion_productos = total_productos - 20

    hoy = datetime.date.today()
    dias = [(hoy - datetime.timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]

    ventas_diarias = []
    for dia in dias:
        total_dia = sum(v['total'] for v in VENTAS if v['fecha'] == dia)
        ventas_diarias.append(total_dia)

    nuevos_clientes_linea = []
    nuevos_productos_linea = []
    for dia in dias:
        cnt_c = sum(1 for c in CLIENTES if c.get('fecha_registro') == dia)
        cnt_p = sum(1 for p in PRODUCTOS if p.get('fecha_registro') == dia)
        nuevos_clientes_linea.append(cnt_c)
        nuevos_productos_linea.append(cnt_p)

    rango1 = sum(1 for p in PRODUCTOS if p['precio'] < 5)
    rango2 = sum(1 for p in PRODUCTOS if 5 <= p['precio'] <= 10)
    rango3 = sum(1 for p in PRODUCTOS if p['precio'] > 10)

    hora_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    return render_template('dashboard.html',
                           total_productos=total_productos,
                           precio_promedio=precio_promedio,
                           total_clientes=total_clientes,
                           ventas_mes=ventas_mes,
                           variacion_productos=variacion_productos,
                           dias=dias,
                           ventas_diarias=ventas_diarias,
                           nuevos_clientes_linea=nuevos_clientes_linea,
                           nuevos_productos_linea=nuevos_productos_linea,
                           rango1=rango1,
                           rango2=rango2,
                           rango3=rango3,
                           hora_actual=hora_actual,
                           ventas=VENTAS)

# ---------- CRUD DE PRODUCTOS ----------
@app.route('/admin/productos')
@login_required
def admin_productos():
    return render_template('admin_productos.html', productos=PRODUCTOS)

@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nuevo_id = max(p['id'] for p in PRODUCTOS) + 1 if PRODUCTOS else 1
        try:
            precio = float(request.form['precio'])
        except ValueError:
            return render_template('producto_form.html', titulo='Nuevo Producto', producto=None, error="Precio inválido")

        producto = {
            'id': nuevo_id,
            'nombre': request.form['nombre'],
            'peso': request.form['peso'],
            'precio': precio,
            'img': request.form['img'],
            'fecha_registro': datetime.date.today().strftime('%d/%m')
        }
        PRODUCTOS.append(producto)
        return redirect(url_for('admin_productos'))
    return render_template('producto_form.html', titulo='Nuevo Producto', producto=None)

@app.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = next((p for p in PRODUCTOS if p['id'] == id), None)
    if not producto:
        return "Producto no encontrado", 404
    if request.method == 'POST':
        try:
            precio = float(request.form['precio'])
        except ValueError:
            return render_template('producto_form.html', titulo='Editar Producto', producto=producto, error="Precio inválido")

        producto['nombre'] = request.form['nombre']
        producto['peso'] = request.form['peso']
        producto['precio'] = precio
        producto['img'] = request.form['img']
        return redirect(url_for('admin_productos'))
    return render_template('producto_form.html', titulo='Editar Producto', producto=producto)

@app.route('/admin/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    global PRODUCTOS
    PRODUCTOS = [p for p in PRODUCTOS if p['id'] != id]
    return redirect(url_for('admin_productos'))

# ---------- CRUD DE CLIENTES ----------
@app.route('/admin/clientes')
@login_required
def admin_clientes():
    return render_template('admin_clientes.html', clientes=CLIENTES)

@app.route('/admin/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    global next_cliente_id
    if request.method == 'POST':
        cliente = {
            'id': next_cliente_id,
            'nombre': request.form['nombre'],
            'email': request.form['email'],
            'telefono': request.form.get('telefono', ''),
            'fecha_registro': datetime.date.today().strftime('%d/%m')
        }
        CLIENTES.append(cliente)
        next_cliente_id += 1
        return redirect(url_for('admin_clientes'))
    return render_template('cliente_form.html', titulo='Nuevo Cliente', cliente=None)

@app.route('/admin/clientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = next((c for c in CLIENTES if c['id'] == id), None)
    if not cliente:
        return "Cliente no encontrado", 404
    if request.method == 'POST':
        cliente['nombre'] = request.form['nombre']
        cliente['email'] = request.form['email']
        cliente['telefono'] = request.form.get('telefono', '')
        return redirect(url_for('admin_clientes'))
    return render_template('cliente_form.html', titulo='Editar Cliente', cliente=cliente)

@app.route('/admin/clientes/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_cliente(id):
    global CLIENTES
    CLIENTES = [c for c in CLIENTES if c['id'] != id]
    return redirect(url_for('admin_clientes'))

# ---------- API REST Y CARRITO ----------
@app.route('/api/productos')
def api_productos():
    return jsonify(PRODUCTOS)

@app.route('/api/carrito/agregar', methods=['POST'])
def api_agregar():
    data = request.get_json() or {}
    producto_id = data.get('id')
    producto = next((p for p in PRODUCTOS if p['id'] == producto_id), None)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404

    carrito = session.get('carrito', {})
    key = str(producto_id)
    if key in carrito:
        carrito[key]['cantidad'] += 1
    else:
        carrito[key] = {
            'id': producto_id,
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': 1
        }
    session['carrito'] = carrito
    session.modified = True
    return jsonify({'carrito': carrito})

@app.route('/api/carrito/eliminar', methods=['POST'])
def api_eliminar():
    data = request.get_json() or {}
    producto_id = str(data.get('id'))
    carrito = session.get('carrito', {})
    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
        else:
            del carrito[producto_id]
    session['carrito'] = carrito
    session.modified = True
    return jsonify({'carrito': carrito})

@app.route('/api/carrito')
def api_ver_carrito():
    return jsonify(session.get('carrito', {}))

# ---------- COMPRA ----------
@app.route('/api/carrito/comprar', methods=['POST'])
def api_comprar():
    global next_venta_id
    carrito = session.get('carrito', {})

    if not carrito:
        return jsonify({'error': 'El carrito está vacío'}), 400

    # Leer JSON ignorando el Content-Type que envíe el cliente
    data = request.get_json(force=True, silent=True) or {}
    metodo_pago = data.get('metodo_pago', 'Efectivo')

    # Calcular total y armar lista de productos
    productos_comprados = []
    total_venta = 0.0
    for item in carrito.values():
        subtotal = item['precio'] * item['cantidad']
        total_venta += subtotal
        productos_comprados.append({
            'nombre': item['nombre'],
            'cantidad': item['cantidad'],
            'precio': item['precio']
        })

    # Registrar la venta  <-- CORRECCIÓN 3: bloque duplicado eliminado
    nueva_venta = {
        'id': next_venta_id,
        'fecha': datetime.date.today().strftime('%d/%m'),
        'productos': productos_comprados,
        'metodo_pago': metodo_pago,
        'total': round(total_venta, 2)
    }
    VENTAS.append(nueva_venta)
    next_venta_id += 1

    # Limpiar el carrito de la sesión
    session.pop('carrito', None)

    return jsonify({'mensaje': f'¡Compra realizada con éxito en la modalidad ({metodo_pago})!'})


if __name__ == '__main__':
    app.run(debug=True)
