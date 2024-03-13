from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Property:
    db_name = "rentdb"
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.address = data['address']
        self.rent = data['rent']
        self.description = data['description']
        self.images = data.get('images', [])
        self.owner_id = data['owner_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create(cls, data):
        query = "INSERT INTO properties (type, address, rent, description, images, owner_id) VALUES (%(type)s, %(address)s, %(rent)s, %(description)s, %(images)s, %(owner_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM properties;"
        results = connectToMySQL(cls.db_name).query_db(query)
        properties = []
        if results:
            for property in results:
                properties.append(property)
            return properties
        return properties
    
    @classmethod
    def get_my_all(cls, data):
        query = "SELECT * FROM properties where owner_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        properties = []
        if results:
            for property in results:
                properties.append(property)
            return properties
        return properties
    
    @classmethod
    def get_property_by_id(cls, data):
        query = 'SELECT * FROM properties left join owners on properties.owner_id = owners.id where properties.id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            query2 = 'SELECT * FROM comments left join renters on comments.renter_id = renters.id WHERE comments.property_id = %(id)s;'
            results2 =  connectToMySQL(cls.db_name).query_db(query2, data)
            comments = []
            if results2:
                for comment in results2:
                    comments.append(comment)
            result[0]['comments'] = comments
            return result[0]
        return False
    
    @classmethod
    def addComment(cls, data):
        query = "INSERT INTO comments (comment, renter_id, property_id) VALUES (%(comment)s, %(renter_id)s, %(property_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_comment_by_id(cls, data):
        query = 'SELECT * FROM comments where id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False
    
    @classmethod
    def deleteAllPostComments(cls, data):
        query = "DELETE FROM comments where comments.property_id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM properties where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def deleteComment(cls, data):
        query = "DELETE FROM comments where id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def updateProperty(cls, data):
        query = "UPDATE properties set type=%(type)s, address = %(address)s, rent = %(rent)s, description = %(description)s, images = %(images)s where properties.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_property(property):
        is_valid = True
        
        if len(property['type'])<1:
            flash("Type of property is required!", 'typeProperty')
            is_valid = False
        if len(property['address'])<3:
            flash("Address is required!", 'addressProperty')
            is_valid = False
        if len(property['description'])<3:
            flash("Description for the property is required!", 'descriptionProperty')
            is_valid = False
        if len(property['rent'])<1:
            flash("Rent is required!", 'rentProperty')
            is_valid = False

        return is_valid
    
    @staticmethod
    def validate_propertyComment(comment):
        is_valid = True
        if len(comment['comment'])< 2:
            flash('comment should be more  or equal to 2 characters', 'renterCommentProperty')
            is_valid = False
        return is_valid