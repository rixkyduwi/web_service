import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "book.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Book(db.Model):

    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def toJson(self):
        return {"title": self.title}

    def __repr__(self):
        return json.dumps(self.__dict__)

@app.after_request
def add_header(response):
    response.headers['X-Expires-At'] = datetime.datetime.now() + datetime.timedelta(days=1, hours=3)
    response.headers['X-Api-Name'] = 'W/S book'
    return response

#curl -i -X GET http://127.0.0.1:4000/books -H 'Content-Type: application/json'
@app.route("/books", methods=["GET"])
def index():
    books = Book.query.all()
    array_books = []
    for book in books:
        dict_books = {}
        dict_books.update({"title": book.title})
        array_books.append(dict_books)
    return jsonify(array_books), 200, {'content-type':'application/json'}        

#curl -i -X POST http://127.0.0.1:4000/books/create -H 'Content-Type: application/json' -d '{"title":"Buku Baru Lagi"}'
@app.route("/books/create", methods=["POST"])
def create():
    req = request.json
    book = Book(title=req['title'])
    db.session.add(book)
    db.session.commit()
    return jsonify(book.toJson()), 201, {'content-type':'application/json'}        

#curl -i -X GET http://127.0.0.1:4000/books/Book-A -H 'Content-Type: application/json'
@app.route("/books/<title>", methods=["GET"])
def show(title):
    book = Book.query.filter_by(title=title).first()
    if(book==None):
        return {"msg": "Book cant be found"}, 404
    else:
        return jsonify(book.toJson()), 200, {'content-type':'application/json'}

# curl -i -X POST http://127.0.0.1:4000/books/update    -H 'Content-Type: application/json'    -d '{"oldtitle":"Bu"}'
# HTTP/1.0 400 BAD REQUEST
# Content-Type: application/json
# Content-Length: 37
# X-Expires-At: 2022-03-11 03:41:51.433542
# X-Api-Name: W/S book
# Server: Werkzeug/0.16.1 Python/3.8.10
# Date: Wed, 09 Mar 2022 17:41:51 GMT

# {
#   "msg": "Error parsing request"
# }
# curl -X POST http://127.0.0.1:4000/books/update    -H 'Content-Type: application/json' -d '{"oldtitle": "Book-1", "newtitle": "Book-A"}'
@app.route("/books/update", methods=["POST"])
def update():
    try:
        req = request.json
        book = Book.query.filter_by(title=req['oldtitle']).first()
        if(book==None):
            return {"msg": "Book cant be found"}, 404
        else:
            book.title = req['newtitle']
            db.session.commit()
            if(book.title!= req['oldtitle']):
                return {"msg": "Book updated"}, 200
            else:
                return {"msg": "Book failed to update"}, 400
    except:
        return {"msg": "Error parsing request"}, 400

@app.route("/books/delete", methods=["DELETE"])
def delete():
    title = request.json['title']
    book = Book.query.filter_by(title=title).first()
    if(book==None):
        return {"msg": "Book cant be found"}, 404
    else: 
        db.session.delete(book)
        db.session.commit()
        book = Book.query.filter_by(title=title).first()
        if(book==None):
            return {"msg": "Succesfully deleted"}, 400
        else:
            return {"msg": "Failed to delete"}, 404

if __name__ == '__main__':
   app.run(debug = True, port=4000)
