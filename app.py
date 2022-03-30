"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretsecret'

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Redirects to User List"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Form to add users"""
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Adds new user to DB and redirects to new users detail page"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"]
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_details(user_id):
    """Show user's detail page"""
    user = User.query.get(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user details form"""
    user = User.query.get(user_id)
    return render_template('edit_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user(user_id):
    """Update data base with new values"""
    user = User.query.get(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """Delete a User"""
    User.query.filter_by(id = user_id).delete()
    db.session.commit()
    return redirect('/users')