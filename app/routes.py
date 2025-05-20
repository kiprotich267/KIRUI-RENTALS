from flask import Blueprint, render_template, redirect, request, session, url_for
from app.forms import RegisterForm, LoginForm, HouseForm

main = Blueprint('main', __name__)

users = {}
houses = [
    {
        'title': 'Modern 2BHK Apartment',
        'location': 'Lahore, Pakistan',
        'price': 'Rs. 45,000/month',
        'image': 'house1.jpg'
    }
]

@main.route('/')
def index():
    return render_template('index.html', houses=houses, username=session.get('username'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.username.data in users:
            return "Username already exists!"
        users[form.username.data] = form.password.data
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if users.get(form.username.data) == form.password.data:
            session['username'] = form.username.data
            return redirect(url_for('main.index'))
        return "Invalid credentials!"
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.index'))

@main.route('/add', methods=['GET', 'POST'])
def add_house():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    form = HouseForm()
    if form.validate_on_submit():
        new_house = {
            'title': form.title.data,
            'location': form.location.data,
            'price': form.price.data,
            'image': form.image.data
        }
        houses.append(new_house)
        return redirect(url_for('main.index'))
    return render_template('add_house.html', form=form)
