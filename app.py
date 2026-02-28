from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la Base de Datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///davidtech.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- CLASE PRODUCTO (POO + SQLite) ---
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

# Crear la base de datos automáticamente
with app.app_context():
    db.create_all()

# --- RUTAS ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inventario')
def gestionar_inventario():
    # Usamos una lista (Colección) para mostrar los productos
    lista_productos = Producto.query.all()
    return render_template('inventario.html', productos=lista_productos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    
    nuevo_prod = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
    db.session.add(nuevo_prod)
    db.session.commit()
    return redirect(url_for('gestionar_inventario'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    prod = Producto.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('gestionar_inventario'))

if __name__ == '__main__':
    app.run(debug=True)