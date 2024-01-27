from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'twoj_sekret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

books = [
    {"id": 1, "title": "Książka 1", "author": "Autor 1", "price": 100},
    {"id": 2, "title": "Książka 2", "author": "Autor 2", "price": 150}
]


@app.route('/')
def index():
    return render_template('index.html', books=books)


@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'cart' not in session:
        session['cart'] = []
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        session['cart'].append(book)
        session.modified = True

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        session['cart'] = []
        session.modified = True
        return redirect(url_for('index'))
    return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)
