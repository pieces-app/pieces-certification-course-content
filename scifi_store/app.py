from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    image_names = [f"stock-{n}.jpeg" for n in range(1, 13)]
    return render_template('home.html', images=image_names, current_page='home')

@app.route('/about')
def about():
    return render_template('about.html', current_page='about')

if __name__ == '__main__':
    app.run(debug=True)
