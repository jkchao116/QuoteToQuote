from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Quote:
    db = "quote_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.quote = data['quote']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']
        self.user = None
        
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO quotes (title,quote,user_id) VALUES(%(title)s,%(quote)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quotes LEFT JOIN USERS ON quotes.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_quotes = []
        for each_quote in results:
            print(each_quote['firstName'])
            this_quote_instance = cls(each_quote)
            one_quote_author_info = {
                "id" : each_quote['id'],
                "firstName" : each_quote['firstName'],
                "last_name" : each_quote['lastName'],
                "email" : each_quote['email'],
                "password" : each_quote['password'],
                "created_at": each_quote['created_at'],
                "updated_at": each_quote['updated_at']
            }
            author = user.User(one_quote_author_info)
            this_qupte_instance.user = author
            all_quote.append(this_quote_instance)
        return all_quotes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM quotes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_one_with_user(cls,data):
        query = "SELECT * FROM quotes JOIN users on users.id = quotes.user_id WHERE quotes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return None
        else:
            one_quote = cls(results[0])
            this_user_dictionary = {
                "id" : results[0]['id'],
                "firstName" : results[0]['firstName'],
                "lastName" : results[0]['lastName'],
                "email" : results[0]['email'],
                "password": results[0]['password'],
                "created_at": results[0]['created_at'],
                "updated_at": results[0]['updated_at']
            }
            quoter = user.User(this_user_dictionary)
            one_quote.user = quoter
            return one_quote
    
    @classmethod
    def update(cls, data):
        query = "UPDATE quotes SET title=%(title)s, quote=%(quote)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM quotes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_quote(sighting):
        is_valid = True
        if len(quote['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters","quote")
        if len(quote['quote']) < 3:
            is_valid = False
            flash("Quote must be at least 3 characters","quote")
        return is_valid