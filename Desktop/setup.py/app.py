from flask import Flask, render_template, request, redirect, url_for, flash
from src.data import db_handler
from src.core import auth 

app = Flask(__name__)
app.secret_key = "clave_secreta_banco_sol"

# 1. RUTA LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario'] # El usuario debe poner la Cédula (Ej: V-12345)
        clave_input = request.form['clave']

        datos_usuario = db_handler.buscar_usuario(usuario_input)
        
        if datos_usuario:
            clave_real = db_handler.obtener_clave(usuario_input)
            if clave_input == clave_real:
                return redirect(url_for('dashboard', nombre=datos_usuario[0]))
            else:
                flash("Contraseña incorrecta")
        else:
            flash("Usuario no encontrado (Recuerda usar tu Cédula completa Ej: V-12345678, E-123456789, J-1234567890)")

    return render_template('login.html')

# 2. RUTA REGISTRO (NUEVA)
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Capturamos datos del formulario web
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        cedula_num = request.form['cedula']
        telefono = request.form['telefono']
        email = request.form['email']
        clave = request.form['clave']

        # 1. Armamos el texto completo para tu validador (Ej: "V-12345678")
        texto_a_validar = f"{tipo}-{cedula_num}"

        # 2. Usamos la funcion "validar_identificador" de mi archivo auth.py
        # La función devuelve 4 cosas: (valido, tipo_limpio, numero_limpio, mensaje)
        es_valido, tipo_detectado, numero_detectado, mensaje_error = auth.validar_identificador(texto_a_validar)

        if not es_valido:
            flash(mensaje_error) # Aquí se muestra el mensaje de error ("Error! la cedula debe tener...")
            return redirect(url_for('registro'))

        # 3. Si pasa la prueba, reconstruimos el documento final
        documento_final = f"{tipo_detectado}-{numero_detectado}"

        #Aqui van el resto de validaciones (Teléfono, Email, Clave) ---
        valido_tlf, msg_tlf = auth.validar_telefono(telefono)
        if not valido_tlf:
            flash(msg_tlf)
            return redirect(url_for('registro'))

        valido_mail, msg_mail = auth.validar_email(email)
        if not valido_mail:
            flash(msg_mail)
            return redirect(url_for('registro'))
            
        valido_clave, msg_clave = auth.validar_clave(clave)
        if not valido_clave:
            flash(msg_clave)
            return redirect(url_for('registro'))

        # 4. Aqui se guarda en la base de datos
        if db_handler.registrar_usuario(nombre, documento_final, tipo, telefono, email, clave):
            flash("¡Registro exitoso! Ahora inicia sesión.")
            return redirect(url_for('login'))
        else:
            flash("Error: Esa cédula ya está registrada.")

    return render_template('registro.html')

# 3. RUTA DASHBOARD
@app.route('/dashboard/<nombre>')
def dashboard(nombre):
    return f"<h1>¡Bienvenido a tu Banco, {nombre}! </h1><p>Sistema Web Activo.</p>"

if __name__ == '__main__':
    db_handler.inicializar_db() 
    app.run(debug=True, port=5000)