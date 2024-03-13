from flask_app import app
from flask import render_template, request, session, redirect, flash,jsonify
from flask_bcrypt import Bcrypt 
from flask_app.models.renter import Renter
from flask_app.models.property import Property
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'renter_id' in session:
        return redirect('/renter/dashboard')
    return redirect('/logout')

@app.route('/register/renter', methods = ['POST'])
def register():
    if 'renter_id' in session:
        return redirect('/')
    if not Renter.validate_renterRegister(request.form):
        return redirect(request.referrer)
    renter = Renter.get_renter_by_email(request.form)
    if renter:
        flash('This account already exists', 'renterEmailRegister')
        return redirect(request.referrer)
    
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'description': request.form['description'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['renter_id'] = Renter.create(data)
    return redirect('/')


@app.route('/login')
def loginPage():
    if 'renter_id' in session:
        return redirect('/renter/dashboard')
    return render_template('renterLoginRegister.html')


@app.route('/login/renter', methods = ['POST'])
def login():
    if 'renter_id' in session:
        return redirect('/')
    if not Renter.validate_renter(request.form):
        return redirect(request.referrer)
    renter = Renter.get_renter_by_email(request.form)
    if not renter:
        flash('This email doesnt exist', 'renterEmailLogin')
        return redirect(request.referrer)
    
    if not bcrypt.check_password_hash(renter['password'], request.form['password']):
        flash('Incorrect password', 'renterPasswordLogin')
        return redirect(request.referrer)
    
    session['renter_id']= renter['id']
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/renter/dashboard')
def dashboardRenter():
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        'id': session['renter_id']
    }
    renter = Renter.get_renter_by_id(data)
    print(renter)
    properties = Property.get_all()
    return render_template('renterdashboard.html', loggedRenter = renter, properties=properties)

@app.route('/renter/profile')
def renterProfile():
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        'id': session['renter_id']

    }
    
    loggedRenter = Renter.get_renter_by_id(data)
    return render_template('renterProfile.html', loggedRenter = loggedRenter)

@app.route('/renter/editprofile')
def renterEditProfile():
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        'id': session['renter_id'],

    }
    renter = Renter.get_renter_by_id(data)
    
    return render_template('renterEditProfile.html', loggedRenter = renter)

@app.route('/renter/editprofile', methods = ['POST'])
def updateRenterProfile():
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        'id': session['renter_id']
    }
    renter = Renter.get_renter_by_id(data)
    if renter['id'] == session['renter_id']:
        if not Renter.validate_renterUpdate(request.form):
            return redirect(request.referrer)
        data = {
            'email': request.form['email'],
         
            'description': request.form['description'],
            'id': session['renter_id']
            
        }
        Renter.update(data)
        return redirect('/renter/profile')
    return redirect('/')