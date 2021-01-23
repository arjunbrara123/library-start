from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy.orm import session

app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
app.secret_key = "test123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
sa_url = 'sqlite:///new-books-collection.db'

# Create table class object
class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(250), unique=True, nullable=False)
   author = db.Column(db.String(250), unique=False, nullable=False)
   rating = db.Column(db.Float, unique=False, nullable=False)

   def __repr__(self):
       return '<Book %r>' % self.title


# Adding entry
def add_entry(title, author, rating):
    new_book = Book(title=title, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()

# Update entry
def update_entry(book_id, title=None, author=None, rating=None):
    book_to_update = Book.query.get(book_id)
    if title != None: book_to_update.title = title
    if author != None: book_to_update.author = author
    if rating != None: book_to_update.rating = rating
    db.session.commit()

# Delete entry
def delete_entry(book_id):
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

# Get Book from ID
def get_book(book_id):
    book = Book.query.get(book_id)
    return book

# {"name": "Excelling at Automations", "author": "Arjun", "rating": "11/10"}
def refresh_db():
    return db.session.query(Book).all()

all_books = refresh_db()

@app.route('/')
def home():
    if request.method == "DELETE":
        delete_entry(request.form['id'])
    all_books = refresh_db()
    return render_template('index.html', books=all_books)


@app.route('/delete/<book_id>')
def delete(book_id):
    #book = get_book(book_id)
    delete_entry(book_id)
    return redirect(url_for('home'))


@app.route('/edit/<book_id>')
def edit(book_id):
    book = get_book(book_id)
    msg = ""
    if str(request.args.get('rating')) != "None":
        update_entry(request.args.get('id'), rating=request.args.get('rating'))
        msg = "Book rating updated to: " + str(request.args.get('rating'))
        flash(msg)
    return render_template('edit.html', book=book, msg=msg)


@app.route("/add", methods=('GET', 'POST'))
def add():
    msg = ""
    if request.method == "POST":
        print("Test 01")
        book = {
            "title": request.form['title'],
            "author": request.form['author'],
            "rating": request.form['rating']
        }
        add_entry(request.form['title'], request.form['author'], request.form['rating'])
        all_books = refresh_db()
        msg = f"Book {book['title']} by {book['author']} was successfully added."
    return render_template('add.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True)
