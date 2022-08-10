from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask_app.models import quote
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    db = "quote_schema"
    def __init__(self,data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.quote = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (firstName, lastName, email, password) VALUES(%(firstName)s,%(lastName)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email already exists.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is Invalid","register")
            is_valid=False
        if len(user['firstName']) < 2:
            flash("First name must be at least 2 characters","register")
            is_valid= False
        if len(user['lastName']) < 2:
            flash("Last name must be at least 2 characters","register")
            is_valid= False
        if len(user['password']) < 6:
            flash("Password must be at least 6 characters","register")
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match","register")
            is_valid= False
        if re.search('[0-9]',user['password']) is None:
            flash("Password must contain at least 1 number", "register")
            is_valid= False
        if re.search('[a-zA-Z]', user['password']) is None:
            flash("Password must contain at least 1 letter", "register")
        return is_valid

    
        