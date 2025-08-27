from flask import Flask, request, jsonify,render_template,redirect
import db
from db import add_book, borrow_book, return_book, list_books

app = Flask(__name__)

@app.route("/")
def index():
    books = db.list_books()
    users = db.list_users()
    return render_template("index.html",books = books, users = users)

@app.route("/add",methods = ["POST"])
def add():
    bookname = request.form["bookname"]
    author = request.form["author"]
    db.add_book(bookname,author)
    return redirect("/")

@app.route("/books",methods = ["GET"])
def get_books():
    return jsonify(list_books())

@app.route("/addBook",methods = ["POST"])
def add_book_api():
    data = request.json
    book_id = add_book(data["bookname"],data["author"])
    return jsonify({"message":"Book added","book_id":book_id})

@app.route("/borrowBook",methods = ["POST"])
def borrow_api():
    data= request.json
    result = borrow_book(data["user_id"],data["book_id"])
    return jsonify({"message":result})

@app.route("/returnBook",methods = ["POST"])
def return_api():
    data = request.json
    result = return_book(data["user_id"],data["book_id"])
    return jsonify({"message":result})

@app.route("/borrowForm",methods=["POST"])
def borrow_form():
    user_id = request.form["user_id"]
    book_id = request.form["book_id"]
    result = borrow_book(user_id,book_id)
    return redirect("/")

@app.route("/returnForm",methods=["POST"])
def return_form():
    user_id = request.form["user_id"]
    book_id = request.form["book_id"]
    result = return_book(user_id,book_id)
    return redirect("/")

@app.route("/addUser",methods=["POST"])
def add_user_form():
    name = request.form["name"]
    user_type = request.form["user_type"]
    db.add_user(name,user_type)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)