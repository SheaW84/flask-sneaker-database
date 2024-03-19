from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/sign_up', methods = ['GET','POST'])
def sign_up():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}','User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form=form)

@auth.route('/login', methods =['GET','POST'])
def login():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You logged in successfully!','auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your credentials couldn not be verified','auth-failed')
    except:
        raise Exception('Invalid data')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out")
    return redirect(url_for('site.home'))