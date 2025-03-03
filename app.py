from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bookstore'
mongo = PyMongo(app)

@app.route('/')
def index():
    books = mongo.db.books.find()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        quantity = request.form['quantity']
        id = request.form['id']
        
        mongo.db.books.insert_one({
            'title': title,
            'author': author,
            'price': float(price),
            'quantity': int(quantity),
            'id': int(id)
        })
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = mongo.db.books.find_one({'_id': book_id})
    if request.method == 'POST':
        mongo.db.books.update_one(
            {'_id': book_id},
            {'$set': {
                'title': request.form['title'],
                'author': request.form['author'],
                'price': float(request.form['price']),
                'quantity': int(request.form['quantity']),
                'id': int(request.form['id'])
            }}
        )
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<book_id>')
def delete_book(book_id):
    mongo.db.books.delete_one({'_id': book_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
