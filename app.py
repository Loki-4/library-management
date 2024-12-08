from flask import Flask, request, jsonify
from models import Book, Member
from auth import token_required

app = Flask(__name__)
@app.route('/')
def home():
    return "Welcome to the Library Management System API!"

books = []
members = []


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(id=len(books)+1, **data)
    books.append(new_book)
    return jsonify({"message": "Book added"}), 201

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify([book.__dict__ for book in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((b for b in books if b.id == id), None)
    if book:
        return jsonify(book.__dict__)
    return jsonify({"message": "Book not found"}), 404

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = next((b for b in books if b.id == id), None)
    if book:
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        return jsonify({"message": "Book updated"})
    return jsonify({"message": "Book not found"}), 404

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    books = [b for b in books if b.id != id]
    return jsonify({"message": "Book deleted"})


@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    result = [book.__dict__ for book in books if query.lower() in book.title.lower() or query.lower() in book.author.lower()]
    return jsonify(result)


@app.route('/books', methods=['GET'])
def get_books_paginated():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify([book.__dict__ for book in books[start:end]])

@app.route('/secure', methods=['GET'])
@token_required
def secure_area():
    return jsonify({"message": "This is a secure area"})

if __name__ == '__main__':
    app.run(debug=True)
