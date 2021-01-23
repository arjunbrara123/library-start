from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy.orm import session

app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
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

# {"name": "Excelling at Automations", "author": "Arjun", "rating": "11/10"}
all_books = db.session.query(Book).all()


@app.route('/')
def home():
    return render_template('index.html', books=all_books)


@app.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == "POST":
        print("Test 01")
        book = {
            "title": request.form['title'],
            "author": request.form['author'],
            "rating": request.form['rating']
        }
        add_entry(request.form['title'], request.form['author'], request.form['rating'])
        all_books.append(book)
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
