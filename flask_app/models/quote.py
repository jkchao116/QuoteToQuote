from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Quote:
    db = "quote"
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
        query = "INSERT INTO quote (title,quote,user_id) VALUES(%(title)s,%(quote)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quote LEFT JOIN USERS ON quote.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        all_quotes = []
        for each_quote in results:
            print(each_quote['firstName'])
            this_quote_instance = cls(each_quote)
            one_quote_author_info = {
                "id" : each_quote['id'],
                "firstName" : each_quote['firstName'],
                "lastName" : each_quote['lastName'],
                "email" : each_quote['email'],
                "password" : each_quote['password'],
                "createdAt": each_quote['createdAt'],
                "updatedAt": each_quote['updatedAt']
            }
            author = user.User(one_quote_author_info)
            this_qupte_instance.user = author
            all_quotes.append(this_quote_instance)
        return all_quotes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM quote WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )
    
    @classmethod
    def get_one_with_user(cls,data):
        query = "SELECT * FROM quote JOIN users on users.id = quote.user_id WHERE quote.id = %(id)s;"
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
                "createdAt": results[0]['createdAt'],
                "updatedAt": results[0]['updatedAt']
            }
            quoter = user.User(this_user_dictionary)
            one_quote.user = quoter
            return one_quote
    
    @classmethod
    def update(cls, data):
        query = "UPDATE quote SET title=%(title)s, quote=%(quote)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM quote WHERE id = %(id)s;"
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