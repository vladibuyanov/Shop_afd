from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6c25d2b8081e4df4f6c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# import os
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')

db = SQLAlchemy(app)
manager = LoginManager(app)


# Database models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(5), nullable=False)
    about = db.Column(db.Text, nullable=False)
    size = db.Column(db.String(50), nullable=False)
    src = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    isActive = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return self.title


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Main page
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index_test():
    items = Item.query.all()  # .order_by(Item.name).
    return render_template('index.html', db=items)


@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        item = Item(
            title=request.form['title'],
            price=request.form['price'],
            about=request.form['about'],
            size=request.form['size'],
            src=request.form['src'],
            link=request.form['link']
        )
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/index')
        except Warning:
            return "Something is going wrong"
    else:
        return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page)
        else:
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_test'))


@app.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


if __name__ == '__main__':
    app.run()
