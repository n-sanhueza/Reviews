from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app


#IMPORTAMOS TODOS LOS MODELOS

from flask_app.models.users import User
from flask_app.models.reviews import Review

#importamos BCrypt --> Encriptamos la contraseña
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt (app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    #request.for ={recibo un diccionario con la información del formulario}

    #validaos que la info sea correcta
    if not User.validate_user(request.form):
        #No es valida la info, redirecciono al formulario
        return redirect("/")
    
    #Encriptar la contraseña
    pass_encrypt = bcrypt.generate_password_hash(request.form["password"])
    #Generamos un diccionario con toda la info y la contraseña encriptada
    form ={
        "first_name":request.form['first_name'],
        "last_name" :request.form['last_name'],
        "email": request.form['email'],
        "password": pass_encrypt
    }

    nuevo_id =User.save(form) #Recibimos el ID del nuevo Usuario
    session['user_id'] = nuevo_id
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    #Verificar que el usuario inició sesión
    if 'user_id' not in session:
        return redirect("/")
    
    #Crear una instancia del usuario en base a la sesión
    form = {"id": session['user_id']}
    user = User.get_by_id(form)

    #PENDIENTE : LISTA RESEÑAS
    reviews =Review.get_all()
    all_users = User.get_all()
    
    
    return render_template("dashboard.html", user = user, reviews=reviews, all_users= all_users)


@app.route("/login", methods=['POST'])
def login():
    #request.form = {"email": "elena@cd.com", "password": "Hola123"}
    #Verificamos que el email exista en BD
    user = User.get_by_email(request.form) #user = instancia User O False

    if not user:
        flash("E-mail no registrado", "login")
        return redirect("/")
    
    #Si user SI es instancia de User
    if not bcrypt.check_password_hash(user.password, request.form['password']): #contra encryptada, contra no encr
        flash("Password incorrecto", "login")
        return redirect("/")
    
    session['user_id'] = user.id #Guardo en sesión el ID del usuario
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/reset_password", methods=['GET'])
def reset_password_form():
    return render_template("password.html")

@app.route("/reset_password", methods=['POST'])
def reset_password():
    # Verificar si el correo electrónico existe en la base de datos
    user = User.get_by_email(request.form['email'])
    
    if not user:
        flash("Correo electrónico no registrado", "password")
        return redirect("/")
    
    session['reset_email'] = request.form['email']
    return redirect("/")




        