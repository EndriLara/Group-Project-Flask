from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Renter:
    db_name = "rentdb"
    def __init__(self, data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.description = data['description']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_renter_by_email(cls, data):
        query = 'SELECT * FROM renters where email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_renter_by_id(cls, data):
        query = 'SELECT * FROM renters where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_renter_by_renter_id(cls, data):
        query = 'SELECT * FROM renters where id = %(renter_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
        
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO renters (firstName, lastName, description, email, password) VALUES (%(firstName)s, %(lastName)s, %(description)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE renters set email = %(email)s, description = %(description)s WHERE renters.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_renter(renter):
        is_valid = True
        if not EMAIL_REGEX.match(renter['email']): 
            flash("Invalid email address!", 'renterEmailLogin')
            is_valid = False
        if len(renter['password'])<8:
            flash("Password is required!", 'renterPasswordLogin')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_renterRegister(renter):
        is_valid = True
        if not EMAIL_REGEX.match(renter['email']): 
            flash("Invalid email address!", 'renterEmailRegister')
            is_valid = False
        if len(renter['password'])<8:
            flash("Password should be minimum 8 characters!", 'renterPasswordRegister')
            is_valid = False 
 
        if len(renter['confirm_password'])<8:
            flash("Confirm Password should be minimum 8 characters!", 'renterConfirmPasswordRegister')
            is_valid = False  
        if renter['password'] != renter['confirm_password']:
            flash("Your password is different from the confirmed password ", 'errorRenterPasswordRegister')   
            is_valid = False 
        
        if len(renter['firstName'])<1:
            flash("First name is required!", 'renterNameRegister')
            is_valid = False
        if len(renter['lastName'])<1:
            flash("Last name is required!", 'renterlastNameRegister')
            is_valid = False
        if len(renter['description'])<10:
            flash("Description should be minimum 10 characters!", 'renterDescriptionRegister')
            is_valid = False 
        return is_valid
    @staticmethod
    def validate_renterUpdate(renter):
        is_valid = True
        if not EMAIL_REGEX.match(renter['email']): 
            flash("Invalid email address!", 'renterEmaiEdit')
            is_valid = False
        if len(renter['description'])<10:
            flash("Description should be minimum 10 characters!", 'renterDescriptionEdit')
            is_valid = False 
        return is_valid