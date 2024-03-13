from flask_app import app
from flask import render_template, request, session, redirect, flash,jsonify
from flask_bcrypt import Bcrypt 
from flask_app.models.owner import Owner
from flask_app.models.property import Property
from flask_app.models.renter import Renter
bcrypt = Bcrypt(app)

from datetime import datetime
from urllib.parse import unquote
UPLOAD_FOLDER = 'flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
from werkzeug.exceptions import RequestEntityTooLarge

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import urllib.parse

import smtplib


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/owner/properties/new')
def newProperty():
    if 'owner_id' not in session:
        return redirect('/propertyOwner')
    data = {
        'owner_id': session['owner_id']
    }
    return render_template('newProperty.html',loggedOwner = Owner.get_owner_by_id(data) )


@app.route('/owner/properties/create', methods = ['POST'])
def createProperty():
    if 'owner_id' not in session:
        return redirect('/propertyOwner')
    if not Property.validate_property(request.form):
        return redirect(request.referrer)
    if 'images' not in request.files:
        flash('Please upload an image', 'imagesProperty')
        return redirect(request.referrer)
    propertyImages = request.files.getlist('images')
    image_filenames = []
    for propertyimage in propertyImages:
        if not allowed_file(propertyimage.filename):
            flash('The file should be in png, jpg or jpeg format!', 'imagesProperty')
            return redirect(request.referrer)
    
        if propertyimage:
            filename1 = secure_filename(propertyimage.filename)
            time = datetime.now().strftime("%d%m%Y%S%f")
            time += filename1
            filename1 = time
            propertyimage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            image_filenames.append(filename1)
            
    images_string = ','.join(image_filenames)
            
        
    data = {
        'type': request.form['type'],
        'address': request.form['address'],
        'rent': request.form['rent'],
        'description': request.form['description'],
        'images': images_string,
        'owner_id': session['owner_id']
    }
    Property.create(data)
    return redirect('/propertyOwner')
    

@app.route('/owner/properties/<int:id>')
def showOneProperty(id):
    if 'owner_id' not in session:
        return redirect('/propertyOwner')
    data = {
        'owner_id':session['owner_id'],
        'id': id
    }
    owner = Owner.get_owner_by_id(data)
    property = Property.get_property_by_id(data)
    return render_template('ownerProperty.html', property=property, loggedOwner = owner)


@app.route('/renter/delete/comment/<int:id>')
def deleteComment(id):
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    comment = Property.get_comment_by_id(data)
    
    if comment['renter_id'] == session['renter_id']:
        Property.deleteComment(data)
    return redirect(request.referrer)

@app.route('/renter/comments/add/<int:id>', methods = ['POST'])
def createComment(id):
    if 'renter_id' not in session:
        return redirect('/')
    if not Property.validate_propertyComment(request.form):
        return redirect(request.referrer)
    data = {
        'renter_id': session['renter_id'],
        'property_id': id,
        'comment': request.form['comment']
    }
    Property.addComment(data)
    return redirect(request.referrer)

@app.route('/renter/properties/<int:id>')
def showOneRenterProperty(id):
    if 'renter_id' not in session:
        return redirect('/')
    data = {
        
        'id': id
    }
    
    property = Property.get_property_by_id(data)
    
    return render_template('renterProperty.html', property=property)

@app.route('/owner/properties/delete/<int:id>')
def deleteProperty(id):
    if 'owner_id' not in session:
        return redirect('/propertyOwner')
    data = {
        
        'id': id
    }
    property = Property.get_property_by_id(data)
    if property['owner_id'] == session['owner_id']:
        Property.deleteAllPostComments(data)
        Property.delete(data)
    return redirect('/propertyOwner')