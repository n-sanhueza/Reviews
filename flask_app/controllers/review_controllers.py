from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

from flask_app.models.users import User
from flask_app.models.reviews import Review

@app.route('/new/review')
def new_review():
    if 'user_id' not in session:
        return redirect("/")
    
    return render_template('new.html')

@app.route("/create/review", methods =['POST'])
def create():
    if 'user_id' not in session:
        return redirect("/")
    
    #Validar info reseña
    if not Review.validate_review(request.form):
        return redirect ("/new/review")

    #guardar la reseña y redirect a dashboard
    Review.save(request.form)
    return redirect("/dashboard")

@app.route("/show/<int:review_id>")
def show_review(review_id):
    if 'user_id' not in session:
        return redirect("/")
    
    review = Review.get_by_id(review_id)  # Aquí utilizamos review_id
    if not review:
        flash("La reseña no fue encontrada", "error")
        return redirect("/dashboard")
    
    return render_template("show.html", review=review)

@app.route("/profile")
def profile():
    #Verificar que el usuario inició sesión
    if 'user_id' not in session:
        return redirect("/")
    
    #Crear una instancia del usuario en base a la sesión
    form = {"id": session['user_id']}
    user = User.get_by_id(form)

    #PENDIENTE : LISTA RESEÑAS
    reviews =Review.get_all_id()

    return render_template('profile.html', user= user, reviews= reviews)

@app.route("/edit/<int:id>")
def edit(id):
    #Verificar que el usuario inició sesión
    if 'user_id' not in session:
        return redirect("/")
    
    diccionario = {'id': id}
    review = Review.get_by_review(diccionario)

    return render_template('edit.html', review = review)

@app.route("/update/review", methods = ['POST'])
def update_review():
    if 'user_id' not in session:
        return redirect("/")
    #Validar info reseña
    if not Review.validate_review(request.form):
        return redirect ("/edit/"+request.form['id'])
    
    #Actualizar el registro
    Review.update(request.form)
    return redirect ('/dashboard')

@app.route("/delete/<int:id>")
def delete(id):
    #Verificar que el usuario inició sesión
    if 'user_id' not in session:
        return redirect("/")   
    #borrar reseña
    form = {"id":id}
    Review.delete(form)
    return redirect ("/profile")











