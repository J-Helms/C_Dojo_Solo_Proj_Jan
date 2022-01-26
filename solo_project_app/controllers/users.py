from solo_project_app import app
from flask import render_template, redirect, session, request, flash
from solo_project_app.models.user import User
from solo_project_app.models.pet import Pet
from solo_project_app.controllers import pets
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def go_to():
    return redirect('/login_reg')


@app.route('/login_reg')
def user_login():
    return render_template('login_reg.html')


@app.route('/login/complete', methods=['POST'])
def user_login_complete():
    data = {
        'username' : request.form['username']
    }
    user_info = User.get_user_by_username(data)
    if not user_info:
        flash("Invalid Login Information")
        return redirect('/login')
    if not bcrypt.check_password_hash(user_info.password, request.form['password']):
        flash("Invalid Login Information")
        return redirect('/login')
    session['active_user'] = user_info.id
    return redirect("/dashboard")


@app.route('/register/complete', methods = ['POST'])
def user_register_complete():
    if not User.validate_user_register(request.form):
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'username' : request.form['username'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'password' : pw_hash
    }
    session['active_user'] = User.save(data)
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if not 'active_user' in session:
        flash("You must be logged in to visit this page. Please Login or Register.")
        return redirect('/login')
    data = {
        'id' : session['active_user']
    }
    user = User.get_one_user(data)
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_reg')
