import json
import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
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
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    
    # 1. Guardar en la Base de Datos (SQLite)
    nuevo_prod = Producto(nombre=nombre, cantidad=int(cantidad), precio=float(precio))
    db.session.add(nuevo_prod)
    db.session.commit()

    # Rutas para los archivos
    ruta_txt = 'inventario/data/datos.txt'
    ruta_json = 'inventario/data/datos.json'
    ruta_csv = 'inventario/data/datos.csv'

    # 2. Guardar en TXT
    with open(ruta_txt, 'a') as f:
        f.write(f"Producto: {nombre}, Cantidad: {cantidad}, Precio: {precio}\n")

    # 3. Guardar en JSON (como lista de diccionarios)
    datos_json = []
    if os.path.exists(ruta_json) and os.path.getsize(ruta_json) > 0:
        with open(ruta_json, 'r') as f:
            datos_json = json.load(f)
    
    datos_json.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
    with open(ruta_json, 'w') as f:
        json.dump(datos_json, f, indent=4)

    # 4. Guardar en CSV
    with open(ruta_csv, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, cantidad, precio])

    return redirect(url_for('gestionar_inventario'))

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    prod = Producto.query.get(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('gestionar_inventario'))

@app.route('/datos')
def mostrar_datos_archivo():
    contenido = []
    # Verificamos si el archivo existe para no tener errores
    if os.path.exists('inventario/data/datos.json'):
        with open('inventario/data/datos.json', 'r') as f:
            try:
                contenido = json.load(f)
            except:
                contenido = []
    return render_template('datos.html', productos_archivo=contenido)
56:with app.app_context():
57:    db.create_all()  
58:
59:if __name__ == '__main__':
60:    app.run(debug=True)