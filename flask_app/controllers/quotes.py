from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

#Route that will show the report form
@app.route('/new/quote')
def create_quote():
    if 'user_id' not in session:
            return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    
    return render_template("new_quote.html", user = User.get_by_id(data))

#Route that will show the edit form
@app.route('/edit/<int:id>')
def edit_quote(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data ={
        'id': id #might need to change this
    }
    user_data ={
        'id' : session['user_id']
    }
    return render_template("edit_quote.html", this_quote = Quote.get_one(data), user=User.get_by_id(user_data))

#Route that will show an individual quote
@app.route('/show/<int:id>')
def view_quote(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id" : session["user_id"]
    }
    return render_template("show_quote.html", this_quote = Quote.get_one_with_user(data), user=User.get_by_id(user_data))

#Route that will delete an individual sighting
@app.route('/delete/<int:id>')
def delete_quote(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data ={
        'id': id
    }
    Quote.destroy(data)
    return redirect("/dashboard")

#Route that will add a sighting to the database (POST)
@app.route('/add/quote/db', methods=['POST'])
def add_quote_db():
    if 'user_id' not in session:
            return redirect('/logout')
    data ={
        'id': session ['user_id']
    }
    
    if not Quote.validate_quote(request.form):
        return redirect("/new/quote")
    data = {
        "title" : request.form["title"],
        "quote" : request.form["quote"],
        "user_id" : session["user_id"]
    }
    Quote.save(data)
    return redirect('/dashboard')

#Route that will edit a quote in the database (POST)
@app.route('/update/quote/<int:id>', methods=['POST'])
def update_quote(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Quote.validate_quote(request.form):
        return redirect('/new/quote')
    data = {
        "title" : request.form["title"],
        "quote" : request.form["quote"],
        "id" : id
    }
    Quote.update(data)
    return redirect('/dashboard')