from flask import Flask, render_template

import db

app = Flask(__name__)

@app.teardown_appcontext
def teardown(exception):
    db.close_connection()

@app.route('/')
def home():
    image_names = [f"stock-{n}.jpeg" for n in range(1, 13)]
    return render_template('home.html', images=image_names, current_page='home')

@app.route('/about')
def about():
    return render_template('about.html', current_page='about')

@app.route('/stock')
def stock():
    stock = db.load_stock(app)
    return render_template('stock.html', stock=stock, current_page='stock')

if __name__ == '__main__':
    db.init_db_if_required(app)
    app.run(debug=True)
