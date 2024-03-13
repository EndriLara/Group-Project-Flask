from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASWORD_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Owner:
    db_name = "rentdb"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.lphone = data['phone']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_owner_by_email(cls, data):
        query = 'SELECT * FROM owners where email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def get_owner_by_id(cls, data):
        query = 'SELECT * FROM owners where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
        
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO owners (first_name, last_name, phone, email, password) VALUES (%(first_name)s, %(last_name)s,  %(phone)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_owner(owner):
        is_valid = True
        if not EMAIL_REGEX.match(owner['email']): 
            flash("Invalid email address!", 'ownerEmailLogin')
            is_valid = False
        if len(owner['password'])<8:
            flash("Password is required!", 'ownerPasswordLogin')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_ownerRegister(owner):
        is_valid = True
        if not EMAIL_REGEX.match(owner['email']): 
            flash("Invalid email address!", 'ownerEmailRegister')
            is_valid = False
        if len(owner['password'])<8:
            flash("Password should be minimum 8 characters!", 'ownerPasswordRegister')
            is_valid = False 
 
        if len(owner['confirm_password'])<8:
            flash("Confirm Password should be minimum 8 characters!", 'ownerConfirmPasswordRegister')
            is_valid = False  
        if owner['password'] != owner['confirm_password']:
            flash("Your password is different from the confirmed password ", 'errorOwnerPasswordRegister')   
            is_valid = False 
        
        if len(owner['first_name'])<1:
            flash("First name is required!", 'ownerNameRegister')
            is_valid = False
        if len(owner['last_name'])<1:
            flash("Last name is required!", 'ownerlastNameRegister')
        if len(owner['phone'])<1:
            flash("Phone is required!", 'ownerPhoneRegister')
            is_valid = False
            
        return is_valid