from flask import Flask

app = Flask(__name__)

# 1. Ruta principal (Home)
@app.route('/')
def inicio():
    return '''
        <h1>Bienvenido a DavidTech – Innovación y Repuestos</h1>
        <p>Estado del Servidor: <b>En línea</b></p>
        <hr>
        <p>Consulta un producto usando la ruta: <i>/producto/nombre-del-item</i></p>
    '''

# 2. Ruta dinámica (Tarea)
@app.route('/producto/<nombre>')
def producto(nombre):
    # Simulamos que el sistema responde según el nombre que pongas en la URL
    return f'''
        <h2>Detalle del Producto</h2>
        <p><b>Producto:</b> {nombre}</p>
        <p><b>Estado:</b> Disponible en bodega principal.</p>
        <a href="/">Volver al inicio</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)