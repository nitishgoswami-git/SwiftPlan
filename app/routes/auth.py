from flask import Blueprint, render_template, request, redirect, url_for , flash, session
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user :
            flash('User already Exists', 'danger')
        else:
            new_user = User(username = username , password = password)
            db.session.add(new_user)
            db.session.commit()

            # Log the user in immediately
            session['user'] = username
            flash('Registration successful! You are now logged in.', 'success')
            return redirect(url_for('task.view_task'))
    return render_template('register.html')

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            session['user'] = username
            flash('Login Successful', 'success')
            return  redirect(url_for('task.view_task'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged Out', 'info')
    return redirect(url_for('auth.login'))