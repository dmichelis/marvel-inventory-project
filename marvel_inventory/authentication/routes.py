from flask import Blueprint, render_template, request, flash, redirect, url_for
from marvel_inventory.forms import UserLoginForm
from marvel_inventory.models import User, db, check_password_hash

from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You made an account {email}' 'That outta show Thanos', 'user-created')

            return redirect(url_for('site.home'))

    except:
        raise Exception('Invalid. Check your stuff')

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password) 

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You have successfully logged in: via email/password', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Check Your Form!')
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))