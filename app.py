import os
from flask import Flask, render_template, request, redirect, url_for
# Librerías nuevas para el Login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# Importamos tu conexión y el modelo de usuario
from Conexion.conexion import obtener_conexion
from models import Usuario

app = Flask(__name__)
app.secret_key = 'clave_secreta_david_tech' # Necesario para mantener la sesión activa

# --- CONFIGURACIÓN DE LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Si alguien no está logueado, lo manda aquí

@login_manager.user_loader
def load_user(user_id):
    db_mysql = obtener_conexion()
    cursor = db_mysql.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    db_mysql.close()
    if user_data:
        return Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
    return None

# --- RUTAS DE INVENTARIO (PROTEGIDAS) ---

@app.route('/inventario')
@login_required # <--- Ahora esta página es privada
def gestionar_inventario():
    try:
        db_mysql = obtener_conexion()
        cursor = db_mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        mis_productos = cursor.fetchall()
        cursor.close()
        db_mysql.close()
        return render_template('inventario.html', productos=mis_productos, usuario=current_user)
    except Exception as e:
        return f"Error de conexión: {e}"

@app.route('/agregar', methods=['POST'])
@login_required
def agregar_producto():
    nombre = request.form.get('nombre')
    cantidad = request.form.get('cantidad')
    precio = request.form.get('precio')
    db_mysql = obtener_conexion()
    cursor = db_mysql.cursor()
    sql = "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, cantidad, precio))
    db_mysql.commit()
    cursor.close()
    db_mysql.close()
    return redirect(url_for('gestionar_inventario'))

# --- RUTAS DE AUTENTICACIÓN (LOGIN Y REGISTRO) ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        db_mysql = obtener_conexion()
        cursor = db_mysql.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
        db_mysql.commit()
        cursor.close()
        db_mysql.close()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db_mysql = obtener_conexion()
        cursor = db_mysql.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, password))
        user_data = cursor.fetchone()
        cursor.close()
        db_mysql.close()
        
        if user_data:
            user = Usuario(user_data['id_usuario'], user_data['nombre'], user_data['email'], user_data['password'])
            login_user(user)
            return redirect(url_for('gestionar_inventario'))
        else:
            return "Correo o contraseña incorrectos. <a href='/login'>Volver</a>"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)