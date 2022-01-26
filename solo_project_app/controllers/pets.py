from solo_project_app import app
from flask import render_template, redirect, session, request, flash
from solo_project_app.models.pet import Pet
from solo_project_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/pet')
def new_pet():
    if not 'active_user' in session:
        flash('You must be logged in to visit this page.Please Login or Register.')
        return redirect('/login')
    data = {
        'id' : session['active_user']
    }
    user = User.get_one_user(data)
    return render_template('create_pet.html', user=user)
    

@app.route('/new/pet/create', methods=['POST'])
def create_pet():
    if not "active_user" in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    data = {
        'pet_name' : request.form['pet_name'],
        'species' : request.form['species'],
        'breed' : request.form['breed'],
        'age' : request.form['age'],
        'fixed' : request.form['fixed'],
        'vet' : request.form['vet'],
        'own_name' : request.form['own_name'],
        'own_call' : request.form['own_call'],
        'own_email' : request.form['own_email'],
        'vacs_rabies_date' : request.form['vacs_rabies_date'],
        'vacs_rabies_duration' : request.form['vacs_rabies_duration'],
        'vacs_bord_date' : request.form['vacs_bord_date'],
        'vacs_bord_duration' : request.form['vacs_bord_duration'],
        'vacs_dis_date' : request.form['vacs_dis_date'],
        'vacs_dis_duration' : request.form['vacs_dis_duration'],
        'vacs_fvrc_date' : request.form['vacs_fvrc_date'],
        'vacs_fvrc_duration' : request.form['vacs_fvrc_duration'],
        'notes' : request.form['notes'],
        'user_id' : session['active_user']
    }
    print(request.form['vacs_fvrc_date'])
    if not Pet.validate_pet(request.form):
        flash('Invalid Entry')
        return redirect('/new/pet')
    id = Pet.create_pet(data)
    return redirect(f'/view/pet/{id}')


@app.route('/view/pet/<int:id>')
def view_pet(id):
    if not 'active_user' in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    data = {
        'id' : id
    }
    user = session['active_user']
    pet = Pet.get_one_pet(data)
    return render_template('view_pet.html', pet=pet, user=user)


@app.route('/view/all/pets')
def view_all_pets():
    if not 'active_user' in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    pets = Pet.get_all_pets
    user = User.get_one_user
    return render_template('view_all_pets.html', user=user, pets=pets)


@app.route('/edit/pet/<int:id>')
def edit_pet(id):
    if not 'active_user' in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    data = {
        'id' : id
    }
    data2 = {
        'id' : session['active_user']
    }
    user = User.get_one_user(data2)
    pet = Pet.get_one_pet(data)
    return render_template('edit_pet.html', pet=pet, user=user)


@app.route('/edit/pet/complete/<int:id>', methods=['POST'])
def edit_pet_complete(id):
    if not 'active_user' in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    data = {
        'id' : id,
        'pet_name' : request.form['pet_name'],
        'species' : request.form['species'],
        'breed' : request.form['breed'],
        'age' : request.form['age'],
        'fixed' : request.form['fixed'],
        'vet' : request.form['vet'],
        'own_name' : request.form['own_name'],
        'own_call' : request.form['own_call'],
        'own_email' : request.form['own_email'],
        'vacs_rabies_date' : request.form['vacs_rabies_date'],
        'vacs_rabies_duration' : request.form['vacs_rabies_duration'],
        'vacs_bord_date' : request.form['vacs_bord_date'],
        'vacs_bord_duration' : request.form['vacs_bord_duration'],
        'vacs_dis_date' : request.form['vacs_dis_date'],
        'vacs_dis_duration' : request.form['vacs_dis_duration'],
        'vacs_fvrc_date' : request.form['vacs_fvrc_date'],
        'vacs_fvrc_duration' : request.form['vacs_fvrc_duration'],
        'notes' : request.form['notes'],
    }
    Pet.update_pet(data)
    return redirect(f'/view/pet/{id}')

@app.route('/delete/pet/<int:id>')
def delete_pet(id):
    if not 'active_user' in session:
        flash('You must be logged in to visit this page. Please Login or Register.')
        return redirect('/login')
    data = {
        'id' : id
    }
    Pet.delete_pet(data)
    return redirect('/view/all/pets')